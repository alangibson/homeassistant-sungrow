"""Exercise sensor selection and values independently of HA lifecycle setup."""
import ast
from dataclasses import dataclass
from pathlib import Path
import runpy
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1] / "custom_components/sungrow"


@dataclass
class Description:
    key: str
    name: str = None
    native_unit_of_measurement: str = None
    device_class: str = None
    state_class: str = None


class Metadata:
    """Supply HA enum names for offline description/selection tests."""
    def __getattr__(self, key):
        return key


def config_namespace():
    namespace = runpy.run_path(str(ROOT / "const.py"))
    namespace.update(dataclass=dataclass, SensorEntityDescription=Description,
                     PERCENTAGE="%")
    for name in ("UnitOfEnergy", "UnitOfPower", "UnitOfElectricPotential",
                 "UnitOfElectricCurrent", "UnitOfTemperature", "UnitOfFrequency",
                 "SensorDeviceClass", "SensorStateClass"):
        namespace[name] = Metadata()
    tree = ast.parse((ROOT / "config.py").read_text())
    tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))]
    exec(compile(tree, "config.py", "exec"), namespace)
    return namespace


def test_sg10rt_exposes_supported_measurements_and_keeps_legacy_keys():
    from test_reader import inverter
    import yaml
    inv = inverter()
    inv.configure_registers(yaml.safe_load((ROOT / "registers-sungrow.yaml").read_text(encoding="utf-8")))
    inv.registers = [r for r in inv.registers if r["type"] == "read" and r["name"] not in ("export_power", "power_meter")]
    descriptions = config_namespace()["supported_sensor_descriptions"](inv)
    keys = [d.key for d in descriptions]
    assert len(keys) == len(set(keys))
    assert {"daily_power_yields", "energy_generation", "array1_energy_generation",
            "array2_energy_generation", "total_active_power", "total_power_yields",
            "phase_a_voltage", "phase_c_current", "internal_temperature", "grid_frequency"} <= set(keys)
    assert not {"export_to_grid", "import_from_grid", "daily_battery_discharge_energy",
                "daily_output_energy", "daily_pv_generation"} & set(keys)


def test_hybrid_duplicate_ids_use_generic_label():
    select = config_namespace()["supported_sensor_descriptions"]
    inv = SimpleNamespace(registers=[{"name": "daily_export_energy"}, {"name": "total_export_energy"}],
                          getInverterModel=lambda: "SH10RT")
    descriptions = select(inv)
    assert [d.name for d in descriptions] == ["Daily Export Energy", "Total Export Energy"]


@pytest.mark.parametrize("model", ["SG10RT", "SH10RT"])
def test_battery_sensors_follow_model_even_with_all_registers_enabled(model):
    namespace = config_namespace()
    all_keys = {d.key for d in namespace["SENSOR_TYPES"]}
    inv = SimpleNamespace(registers=[{"name": key} for key in all_keys],
                          getInverterModel=lambda: model)
    descriptions = namespace["supported_sensor_descriptions"](inv)
    battery = [d for d in descriptions if d.hybrid_only]
    assert bool(battery) == model.startswith("SH")
    assert "daily_export_energy" in {d.key for d in descriptions}
    assert "daily_export_energy" not in namespace["hybrid_only_sensor_keys"]()


def sensor_class():
    namespace = config_namespace()
    tree = ast.parse((ROOT / "sensor.py").read_text())
    entity = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "SungrowInverterSensorEntity")
    # Test value/identity properties against simple coordinator data, without
    # pretending to test HA's registration or scheduling implementation.
    entity.bases = []
    entity.body = [n for n in entity.body if isinstance(n, ast.FunctionDef)
                   and n.name in ("native_value", "unique_id")]
    namespace["logger"] = SimpleNamespace(debug=lambda *args: None)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[entity], type_ignores=[])), "sensor.py", "exec"), namespace)
    return namespace["SungrowInverterSensorEntity"]


@pytest.mark.parametrize("key,data,expected", [
    ("energy_generation", {"total_dc_power": 0}, 0),
    ("array1_energy_generation", {"mppt_1_voltage": 300, "mppt_1_current": 2}, 600),
    ("array2_energy_generation", {"mppt_2_voltage": 300}, None),
    ("total_power_yields", {}, None),
])
def test_sensor_values_and_stable_identity(key, data, expected):
    sensor = sensor_class()()
    sensor._attr_unique_id = None
    sensor.entity_description = SimpleNamespace(key=key, device_id="ABC")
    sensor.coordinator = SimpleNamespace(data=SimpleNamespace(latest_scrape=data))
    assert sensor.native_value == expected
    assert sensor.unique_id == f"sungrow_ABC_{key}"
