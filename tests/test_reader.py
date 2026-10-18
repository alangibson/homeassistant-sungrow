"""Offline protocol regressions using real PyModbus, without HA or hardware."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("reader", ROOT / "custom_components/sungrow/SunGather/inverter.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


def inverter():
    return reader.SungrowInverter(dict(host="offline", port=502, timeout=1,
        retries=0, slave=1, model="SG10RT", level=2, smart_meter=False))


@pytest.mark.parametrize("datatype,words,expected", [
    ("U16", [0], 0), ("U16", [65535], None),
    ("S16", [65535], -1), ("S16", [32767], None),
    ("S16", [32768], -32768), ("U32", [1, 2], 131073),
    ("U32", [65535, 65535], None), ("S32", [65535, 32767], None),
    ("S32", [65535, 65535], -1), ("S32", [0, 32768], -2147483648),
])
def test_decoding_and_invalid_sentinels(datatype, words, expected):
    inv = inverter()
    inv.registers = [dict(name="value", address=5003, type="read", datatype=datatype)]
    inv.latest_scrape = {"value": 123}
    inv.client = Mock()
    inv.client.read_input_registers.return_value = SimpleNamespace(
        registers=words, isError=lambda: False)
    assert inv.load_registers("read", 5002, len(words))
    assert inv.latest_scrape.get("value") == expected
    inv.client.read_input_registers.assert_called_once_with(5002, count=len(words), device_id=1)


def test_partial_poll_drops_old_values_and_preserves_identity():
    inv = inverter()
    inv.latest_scrape = {"serial_number": "ABC", "total_dc_power": 1000, "meter_power": 100}
    inv.registers = [dict(name="total_dc_power", address=5017, datatype="U32", type="read"),
                     dict(name="daily_power_yields", address=5003, datatype="U16", type="read")]
    inv.load_registers = Mock(side_effect=[False, True])
    assert inv.scrape()
    assert inv.latest_scrape["serial_number"] == "ABC"
    assert "total_dc_power" not in inv.latest_scrape
    assert "export_to_grid" not in inv.latest_scrape
    assert "import_from_grid" not in inv.latest_scrape


def test_all_reads_failed_returns_failure():
    inv = inverter()
    inv.registers = [dict(name="daily_power_yields", address=5003, datatype="U16", type="read")]
    inv.load_registers = Mock(return_value=False)
    inv.client = Mock()
    assert inv.scrape() is False
    assert inv.client is None


def test_serial_in_scan_block_uses_its_own_length():
    inv = inverter()
    inv.registers = [dict(name="serial_number", address=4990, type="read", datatype="UTF-8")]
    words = [0] * 40 + [0x4142, 0x4300] + [0] * 8
    inv.client = Mock()
    inv.client.read_input_registers.return_value = SimpleNamespace(registers=words, isError=lambda: False)
    assert inv.load_registers("read", 4949, 50)
    assert inv.latest_scrape["serial_number"] == "ABC"


@pytest.mark.parametrize("meter,exported,imported", [(0, 0, 0), (-500, 500, 0), (200, 0, 200)])
def test_grid_derivation_requires_current_measurement(meter, exported, imported):
    inv = inverter()
    inv.registers = [dict(name="meter_power", address=5083, datatype="S32", type="read")]
    def poll(*args):
        inv.latest_scrape["meter_power"] = meter
        return True
    inv.load_registers = poll
    assert inv.scrape()
    assert inv.latest_scrape["export_to_grid"] == exported
    assert inv.latest_scrape["import_from_grid"] == imported


def test_sg10rt_register_selection_does_not_mutate_packaged_map():
    registers = yaml.safe_load((ROOT / "custom_components/sungrow/registers-sungrow.yaml").read_text(encoding="utf-8"))
    before = repr(registers)
    inv = inverter()
    inv.configure_registers(registers)
    assert repr(registers) == before
    selected = {r["name"] for r in inv.registers}
    assert {"daily_power_yields", "total_power_yields", "total_dc_power", "internal_temperature",
            "phase_a_voltage", "phase_c_current", "mppt_2_current", "grid_frequency"} <= selected
    assert "battery_current" not in selected
