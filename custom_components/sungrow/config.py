from dataclasses import dataclass

from homeassistant.const import (
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfTemperature,
    UnitOfFrequency,
)
from homeassistant.components.sensor import (
    SensorStateClass,
    SensorEntityDescription,
    SensorDeviceClass,
)

from .const import (
    SUNGROW_DAILY_EXPORT_ENERGY,
    SUNGROW_DAILY_POWER_YIELDS,
    SUNGROW_DAILY_PV_EXPORT,
    SUNGROW_ENERGY_GENERATION,
    SUNGROW_ARRAY1_ENERGY_GENERATION,
    SUNGROW_ARRAY2_ENERGY_GENERATION,
    SUNGROW_EXPORT_POWER_HYBRID,
    SUNGROW_POWER_EXPORT_TO_GRID,
    SUNGROW_POWER_IMPORT_FROM_GRID,
    SUNGROW_LOAD_POWER_HYBRID,
    SUNGROW_METER_POWER,
    SUNGROW_SELF_CONSUMPTION_OF_DAY,
    SUNGROW_TOTAL_ACTIVE_POWER,
    SUNGROW_TOTAL_EXPORT_ENERGY,
    SUNGROW_TOTAL_PV_EXPORT,
    SUNGROW_DAILY_OUTPUT_ENERGY,
    SUNGROW_TOTAL_OUTPUT_ENERGY,
    SUNGROW_LOAD_POWER,
    SUNGROW_EXPORT_POWER,
    SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY,
    SUNGROW_TOTAL_BATTERY_CHARGE_PV_ENERGY,
    SUNGROW_DAILY_PV_ENERGY,
    SUNGROW_TOTAL_PV_ENERGY,
    SUNGROW_DAILY_DIRECT_ENERGY_CONSUMPTION,
    SUNGROW_TOTAL_DIRECT_ENERGY_CONSUMPTION,
    SUNGROW_DAILY_IMPORT_ENERGY,
    SUNGROW_TOTAL_IMPORT_ENERGY,
    SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY,
    SUNGROW_TOTAL_BATTERY_DISCHARGE_ENERGY,
    SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV,
    SUNGROW_TOTAL_EXPORT_ENERGY_FROM_PV,
    SUNGROW_DAILY_EXPORT_ENERGY_FROM_BATTERY,
    SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY,
    SUNGROW_DAILY_BATTERY_CHARGE_GRID_ENERGY,
    SUNGROW_TOTAL_BATTERY_CHARGE_GRID_ENERGY,
)


@dataclass
class SungrowInverterSensorEntityDescription(SensorEntityDescription):
    register: str = None
    hybrid_only: bool = False
    device_id: str = None
    device_model: str = None
    _original_name: str = None

    @property
    def original_name(self):
        """Capture original name since we will mutate name later"""
        if not self._original_name:
            self._original_name = self.name
        return self._original_name


SENSOR_TYPES = (
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_ENERGY_GENERATION,
        register=SUNGROW_ENERGY_GENERATION,
        name="Current PV Power Generation",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_ARRAY1_ENERGY_GENERATION,
        register=SUNGROW_ARRAY1_ENERGY_GENERATION,
        name="Current PV Array 1 Power Generation",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_ARRAY2_ENERGY_GENERATION,
        register=SUNGROW_ARRAY2_ENERGY_GENERATION,
        name="Current PV Array 2 Power Generation",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_OUTPUT_ENERGY,
        register=SUNGROW_DAILY_OUTPUT_ENERGY,
        name="Daily Output Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_OUTPUT_ENERGY,
        register=SUNGROW_TOTAL_OUTPUT_ENERGY,
        name="Total Output Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_LOAD_POWER,
        register=SUNGROW_LOAD_POWER,
        name="Current Load Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_LOAD_POWER_HYBRID,
        register=SUNGROW_LOAD_POWER_HYBRID,
        name="Current Load Power (Hybrid)",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_EXPORT_POWER,
        register=SUNGROW_EXPORT_POWER,
        name="Current Export Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_EXPORT_POWER_HYBRID,
        register=SUNGROW_EXPORT_POWER_HYBRID,
        name="Current Export Power (Hybrid)",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_PV_ENERGY,
        register=SUNGROW_DAILY_PV_ENERGY,
        name="Daily PV Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_PV_ENERGY,
        register=SUNGROW_TOTAL_PV_ENERGY,
        name="Total PV Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY,
        register=SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY,
        name="Daily Battery Charge PV Energy",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_BATTERY_CHARGE_PV_ENERGY,
        register=SUNGROW_TOTAL_BATTERY_CHARGE_PV_ENERGY,
        name="Total Battery Charge PV Energy",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_DIRECT_ENERGY_CONSUMPTION,
        register=SUNGROW_DAILY_DIRECT_ENERGY_CONSUMPTION,
        name="Daily Direct Energy Consumption",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_DIRECT_ENERGY_CONSUMPTION,
        register=SUNGROW_TOTAL_DIRECT_ENERGY_CONSUMPTION,
        name="Total Direct Energy Consumption",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_IMPORT_ENERGY,
        register=SUNGROW_DAILY_IMPORT_ENERGY,
        name="Daily Grid Import Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_IMPORT_ENERGY,
        register=SUNGROW_TOTAL_IMPORT_ENERGY,
        name="Total Grid Import Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY,
        register=SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY,
        name="Daily Battery Discharge Energy",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_BATTERY_DISCHARGE_ENERGY,
        register=SUNGROW_TOTAL_BATTERY_DISCHARGE_ENERGY,
        name="Total Battery Discharge Energy",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV,
        register=SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV,
        name="Daily Export Energy From PV",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_PV,
        register=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_PV,
        name="Total Export Energy From PV",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_EXPORT_ENERGY_FROM_BATTERY,
        register=SUNGROW_DAILY_EXPORT_ENERGY_FROM_BATTERY,
        name="Daily Export Energy From Battery",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY,
        register=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY,
        name="Total Export Energy From Battery",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_BATTERY_CHARGE_GRID_ENERGY ,
        register=SUNGROW_DAILY_BATTERY_CHARGE_GRID_ENERGY ,
        name="Daily Battery Charge Energy",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_BATTERY_CHARGE_GRID_ENERGY ,
        register=SUNGROW_TOTAL_BATTERY_CHARGE_GRID_ENERGY ,
        name="Total Battery Charge Energy",
        hybrid_only=True,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ), 
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_EXPORT_ENERGY,
        register=SUNGROW_DAILY_EXPORT_ENERGY,
        name="Daily Export Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_EXPORT_ENERGY,
        register=SUNGROW_TOTAL_EXPORT_ENERGY,
        name="Total Export Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_PV_EXPORT,
        register=SUNGROW_DAILY_PV_EXPORT,
        name="Daily PV Export",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_PV_EXPORT,
        register=SUNGROW_TOTAL_PV_EXPORT,
        name="Total Export Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_SELF_CONSUMPTION_OF_DAY,
        register=SUNGROW_SELF_CONSUMPTION_OF_DAY,
        name="Daily Self Consumption",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_POWER_YIELDS,
        register=SUNGROW_DAILY_POWER_YIELDS,
        name="Daily Energy Yields",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_METER_POWER,
        register=SUNGROW_METER_POWER,
        name="Current Meter Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_ACTIVE_POWER,
        register=SUNGROW_TOTAL_ACTIVE_POWER,
        name="Current Active Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_POWER_EXPORT_TO_GRID,
        register=SUNGROW_POWER_EXPORT_TO_GRID,
        name="Current Power Exported to Grid",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_POWER_IMPORT_FROM_GRID,
        register=SUNGROW_POWER_IMPORT_FROM_GRID,
        name="Current Power Imported from Grid",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    )
)

# Preserve existing keys above; expose the useful input registers that the
# reader already supports. Selection below uses configured registers, never
# the values returned by a single (possibly unsuccessful) poll.
SENSOR_TYPES += tuple(
    SungrowInverterSensorEntityDescription(
        key=key, register=key, name=name,
        native_unit_of_measurement=unit, device_class=device_class,
        state_class=state_class,
    )
    for key, name, unit, device_class, state_class in (
        ("total_power_yields", "Lifetime Energy Yields", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
        ("internal_temperature", "Inverter Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
        ("grid_frequency", "Grid Frequency", UnitOfFrequency.HERTZ, SensorDeviceClass.FREQUENCY, SensorStateClass.MEASUREMENT),
        *((f"mppt_{n}_{kind}", f"MPPT {n} {kind.title()}", unit, device_class, SensorStateClass.MEASUREMENT)
          for n in (1, 2) for kind, unit, device_class in (
              ("voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE),
              ("current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT))),
        *((f"phase_{phase}_{kind}", f"Phase {phase.upper()} {kind.title()}", unit, device_class, SensorStateClass.MEASUREMENT)
          for phase in ("a", "b", "c") for kind, unit, device_class in (
              ("voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE),
              ("current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT))),
        ("work_state_1", "Inverter Work State", None, None, None),
    )
)


def sensor_dependencies(key):
    """Return physical registers needed by a sensor, including derived power."""
    return {
        SUNGROW_ENERGY_GENERATION: ("total_dc_power",),
        SUNGROW_ARRAY1_ENERGY_GENERATION: ("mppt_1_voltage", "mppt_1_current"),
        SUNGROW_ARRAY2_ENERGY_GENERATION: ("mppt_2_voltage", "mppt_2_current"),
        SUNGROW_POWER_EXPORT_TO_GRID: ("export_to_grid",),
        SUNGROW_POWER_IMPORT_FROM_GRID: ("import_from_grid",),
    }.get(key, (key,))


def supported_sensor_descriptions(inverter):
    """Filter unsupported and duplicate legacy sensors without changing IDs."""
    supported = {r["name"] for r in inverter.registers}
    if "meter_power" in supported or "export_power_hybrid" in supported:
        supported.update(("export_to_grid", "import_from_grid"))
    if "load_power_hybrid" in supported or {"meter_power", "total_active_power"} <= supported:
        supported.add("load_power")
    # Last description wins for duplicate legacy battery/export keys, keeping
    # the generic label and the historical unique ID.
    is_hybrid = inverter.getInverterModel().startswith("SH")
    descriptions = {description.key: description for description in SENSOR_TYPES
                    if is_hybrid or not description.hybrid_only}
    return [d for d in descriptions.values() if set(sensor_dependencies(d.key)) <= supported]


def hybrid_only_sensor_keys():
    """Exclude shared export keys that also represent valid non-battery data."""
    hybrid = {d.key for d in SENSOR_TYPES if d.hybrid_only}
    general = {d.key for d in SENSOR_TYPES if not d.hybrid_only}
    return hybrid - general
