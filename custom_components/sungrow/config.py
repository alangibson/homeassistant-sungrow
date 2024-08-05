from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorStateClass
)
from homeassistant.components.sensor import (
    SensorEntityDescription
)
from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    ENERGY_KILO_WATT_HOUR,
    PERCENTAGE,
    POWER_WATT
)
from homeassistant.components.sensor import (
    SensorStateClass,
    SensorEntityDescription,
)
from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    ENERGY_KILO_WATT_HOUR,
    DEVICE_CLASS_POWER,
    POWER_WATT
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
    SUNGROW_DAILY_BATTERY_CHARGE_GRID_ENERGY,
    SUNGROW_TOTAL_BATTERY_CHARGE_GRID_ENERGY,
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
    SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY    
)


@dataclass
class SungrowInverterSensorEntityDescription(SensorEntityDescription):
    register: str = None
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
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_ARRAY1_ENERGY_GENERATION,
        register=SUNGROW_ARRAY1_ENERGY_GENERATION,
        name="Current PV Array 1 Power Generation",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_ARRAY2_ENERGY_GENERATION,
        register=SUNGROW_ARRAY2_ENERGY_GENERATION,
        name="Current PV Array 2 Power Generation",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_OUTPUT_ENERGY,
        register=SUNGROW_DAILY_OUTPUT_ENERGY,
        name="Daily Output Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_OUTPUT_ENERGY,
        register=SUNGROW_TOTAL_OUTPUT_ENERGY,
        name="Total Output Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_LOAD_POWER,
        register=SUNGROW_LOAD_POWER,
        name="Current Load Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_LOAD_POWER_HYBRID,
        register=SUNGROW_LOAD_POWER_HYBRID,
        name="Current Load Power (Hybrid)",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_EXPORT_POWER,
        register=SUNGROW_EXPORT_POWER,
        name="Current Export Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_EXPORT_POWER_HYBRID,
        register=SUNGROW_EXPORT_POWER_HYBRID,
        name="Current Export Power (Hybrid)",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_PV_ENERGY,
        register=SUNGROW_DAILY_PV_ENERGY,
        name="Daily PV Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_PV_ENERGY,
        register=SUNGROW_TOTAL_PV_ENERGY,
        name="Total PV Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY,
        register=SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY,
        name="Daily Battery Charge PV Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_BATTERY_CHARGE_PV_ENERGY,
        register=SUNGROW_TOTAL_BATTERY_CHARGE_PV_ENERGY,
        name="Total Battery Charge PV Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_BATTERY_CHARGE_GRID_ENERGY ,
        register=SUNGROW_DAILY_BATTERY_CHARGE_GRID_ENERGY ,
        name="Daily Battery Charge Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_BATTERY_CHARGE_GRID_ENERGY ,
        register=SUNGROW_TOTAL_BATTERY_CHARGE_GRID_ENERGY ,
        name="Total Battery Charge Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ), 
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_DIRECT_ENERGY_CONSUMPTION,
        register=SUNGROW_DAILY_DIRECT_ENERGY_CONSUMPTION,
        name="Daily Direct Energy Consumption",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_DIRECT_ENERGY_CONSUMPTION,
        register=SUNGROW_TOTAL_DIRECT_ENERGY_CONSUMPTION,
        name="Total Direct Energy Consumption",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_IMPORT_ENERGY,
        register=SUNGROW_DAILY_IMPORT_ENERGY,
        name="Daily Grid Import Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_IMPORT_ENERGY,
        register=SUNGROW_TOTAL_IMPORT_ENERGY,
        name="Total Grid Import Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY,
        register=SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY,
        name="Daily Battery Discharge Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_BATTERY_DISCHARGE_ENERGY,
        register=SUNGROW_TOTAL_BATTERY_DISCHARGE_ENERGY,
        name="Total Battery Discharge Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV,
        register=SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV,
        name="Daily Export Energy From PV",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_PV,
        register=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_PV,
        name="Total Export Energy From PV",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_EXPORT_ENERGY_FROM_BATTERY,
        register=SUNGROW_DAILY_EXPORT_ENERGY_FROM_BATTERY,
        name="Daily Export Energy From Battery",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY,
        register=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY,
        name="Total Export Energy From Battery",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_EXPORT_ENERGY,
        register=SUNGROW_DAILY_EXPORT_ENERGY,
        name="Daily Export Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_EXPORT_ENERGY,
        register=SUNGROW_TOTAL_EXPORT_ENERGY,
        name="Total Export Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_PV_EXPORT,
        register=SUNGROW_DAILY_PV_EXPORT,
        name="Daily PV Export",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_PV_EXPORT,
        register=SUNGROW_TOTAL_PV_EXPORT,
        name="Total Export Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_SELF_CONSUMPTION_OF_DAY,
        register=SUNGROW_SELF_CONSUMPTION_OF_DAY,
        name="Daily Self Consumption",
        native_unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_DAILY_POWER_YIELDS,
        register=SUNGROW_DAILY_POWER_YIELDS,
        name="Daily Energy Yields",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_METER_POWER,
        register=SUNGROW_METER_POWER,
        name="Current Meter Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_TOTAL_ACTIVE_POWER,
        register=SUNGROW_TOTAL_ACTIVE_POWER,
        name="Current Active Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_POWER_EXPORT_TO_GRID,
        register=SUNGROW_POWER_EXPORT_TO_GRID,
        name="Current Power Exported to Grid",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SungrowInverterSensorEntityDescription(
        key=SUNGROW_POWER_IMPORT_FROM_GRID,
        register=SUNGROW_POWER_IMPORT_FROM_GRID,
        name="Current Power Imported from Grid",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    )
)
