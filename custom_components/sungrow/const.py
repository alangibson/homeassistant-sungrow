"""Constants for the Sungrow Inverter integration"""

from datetime import timedelta

DOMAIN = 'sungrow'

DEFAULT_NAME = "Sungrow Inverter"
DEFAULT_PORT = 502
DEFAULT_SLAVE = 0x01
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_TIMEOUT = 10

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

# Unit is W
SUNGROW_ENERGY_GENERATION = "energy_generation"
# Unit is kWh
SUNGROW_ENERGY_CONSUMPTION = "energy_consumption"

SUNGROW_ARRAY1_ENERGY_GENERATION = "array1_energy_generation"
SUNGROW_ARRAY1_VOLTAGE = "array1_voltage"
SUNGROW_ARRAY1_CURRENT = "array1_current"

SUNGROW_ARRAY2_ENERGY_GENERATION = "array2_energy_generation"
SUNGROW_ARRAY2_VOLTAGE = "array2_voltage"
SUNGROW_ARRAY2_CURRENT = "array2_current"

SUNGROW_LOAD_POWER = "load_power"
SUNGROW_LOAD_POWER_HYBRID = "load_power_hybrid"

SUNGROW_EXPORT_POWER = "export_power"
SUNGROW_EXPORT_POWER_HYBRID = "export_power_hybrid"

SUNGROW_DAILY_IMPORT_ENERGY = "daily_import_energy"
SUNGROW_TOTAL_IMPORT_ENERGY = "total_import_energy"

# Battery charged from PV
# TODO these arent real registers.
SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY = "daily_battery_charge_energy_from_pv"
SUNGROW_TOTAL_BATTERY_CHARGE_PV_ENERGY = "total_battery_charge_energy_from_pv"

# Battery charged from GRID
SUNGROW_DAILY_BATTERY_CHARGE_GRID_ENERGY = "daily_charge_energy"
SUNGROW_TOTAL_BATTERY_CHARGE_GRID_ENERGY = "total_charge_energy"

SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY = "daily_battery_discharge_energy"
SUNGROW_TOTAL_BATTERY_DISCHARGE_ENERGY = "total_battery_discharge_energy"

SUNGROW_INVERTER_EFFICENCY = "inverter_efficency"

# TODO these arent real registers.
SUNGROW_DAILY_OUTPUT_ENERGY = "daily_output_energy"
SUNGROW_TOTAL_OUTPUT_ENERGY = "total_output_energy"

SUNGROW_GRID_FREQUENCY = "grid_frequency"

SUNGROW_DAILY_PV_ENERGY = "daily_pv_generation"
SUNGROW_TOTAL_PV_ENERGY = "total_pv_generation"

SUNGROW_DAILY_DIRECT_ENERGY_CONSUMPTION = "daily_direct_energy_consumption"
SUNGROW_TOTAL_DIRECT_ENERGY_CONSUMPTION = "total_direct_energy_consumption"

SUNGROW_DAILY_EXPORT_ENERGY = "daily_export_energy"
SUNGROW_TOTAL_EXPORT_ENERGY = "total_export_energy"

# TODO these arent real registers. Use daily_pv_export, total_pv_export instead?
SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV = "daily_export_power_from_pv"
SUNGROW_TOTAL_EXPORT_ENERGY_FROM_PV = "total_export_power_from_pv"

SUNGROW_DAILY_EXPORT_ENERGY_FROM_BATTERY = "daily_export_energy"
SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY = "total_export_energy"

SUNGROW_SELF_CONSUMPTION_OF_DAY = "self_consumption_of_day"

SUNGROW_DAILY_POWER_YIELDS =  "daily_power_yields" # kWh

SUNGROW_DAILY_PV_EXPORT = "daily_pv_export"
SUNGROW_TOTAL_PV_EXPORT = "total_pv_export"

SUNGROW_METER_POWER = "meter_power"
SUNGROW_TOTAL_ACTIVE_POWER = "total_active_power"

SUNGROW_STATE_BATTERY_CHARGING = "state_battery_charging"
SUNGROW_STATE_BATTERY_DISCHARGING = "state_battery_discharging"
SUNGROW_STATE_FEED_INTO_GRID = "state_feed_into_grid"
SUNGROW_STATE_IMPORT_FROM_GRID = "state_import_from_grid"
SUNGROW_STATE_LOAD_ACTIVE = "state_load_active"

# Synthetic from SunGather
# These are power in W, not energy in kWh
SUNGROW_POWER_EXPORT_TO_GRID = "export_to_grid"
SUNGROW_POWER_IMPORT_FROM_GRID = "import_from_grid"
