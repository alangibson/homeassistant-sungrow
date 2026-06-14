"""Sensor platform integration for Sungrow Inverters"""

from __future__ import annotations

from datetime import timedelta
import logging
import voluptuous as vol
import dataclasses

from homeassistant.components.sensor import (
    SensorEntity
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers import device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity
)
from homeassistant.const import (
    ATTR_MODEL,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PORT,
    CONF_SLAVE,
    CONF_TIMEOUT,
    CONF_HOST,
    CONF_SCAN_INTERVAL,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator
)
from homeassistant.const import (
    CONF_NAME,
    CONF_SCAN_INTERVAL
)

from .const import (
    MIN_TIME_BETWEEN_UPDATES,
    SUNGROW_ENERGY_GENERATION,
    SUNGROW_ARRAY1_ENERGY_GENERATION,
    SUNGROW_ARRAY2_ENERGY_GENERATION,
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SLAVE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT
)

from .config import (
    SENSOR_TYPES,
    SungrowInverterSensorEntityDescription
)

from .inverter import connect_inverter, data_updater

logger = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.string,
        vol.Optional(CONF_SLAVE, default=DEFAULT_SLAVE): cv.positive_int,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(ATTR_MODEL): cv.string,
    }
)


def _require_device_identity(inverter, serial_number: str | None) -> tuple[str, str]:
    """Return inverter serial number and model or raise if identity is incomplete."""
    if not serial_number and inverter:
        serial_number = inverter.latest_scrape.get("serial_number")

    model = inverter.getInverterModel() if inverter else None
    if serial_number and model:
        return serial_number, model

    logger.error(
        "Sungrow inverter setup failed: missing required device identity before "
        "sensor creation (serial_number=%s, model=%s, host=%s)",
        serial_number,
        model,
        inverter.getHost() if inverter else None,
    )
    raise RuntimeError(
        "Sungrow inverter did not report both serial number and model"
    )


# Called automagically by Home Assistant
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    # Get a unique id for the inverter device
    # unique_id is set during the initial configuration step
    unique_device_id = config_entry.data.get('device_id') or config_entry.data.get(
        'serial_number'
    )

    """Setup sensors from a config entry created in the integrations UI."""
    # Configure SungrowInverter
    config_inverter = {
        # client config
        'host': config_entry.data[CONF_HOST],
        'port': config_entry.data.get(CONF_PORT, '502'),
        'timeout': int(config_entry.data.get(CONF_TIMEOUT, 10)),
        'retries': 3,
        'slave': config_entry.data.get(CONF_SLAVE, DEFAULT_SLAVE),
        'serial_number': config_entry.data.get('serial_number'),
        # inverter config
        # None to autodetect, string of model name otherwise
        'model': config_entry.data.get('model'),
        # Information request level
        # 0 = Model and Solar Generation,
        # 1 = Useful data, all required for exports,
        # 2 everything your Inverter supports,
        # 3 Everything from every register
        'level': config_entry.data.get('level', 2),
        # boolean
        'use_local_time': config_entry.data.get('use_local_time', False),
        'smart_meter': config_entry.data.get('smart_meter'),
        'use_scan_ranges': config_entry.data.get('use_scan_ranges', False),
    }

    # Async construct inverter object
    # Make sure we can connect to the inverter
    is_success, inverter = await hass.async_add_executor_job(connect_inverter(config_inverter))
    logger.debug(f'sensor async_setup_entry is_connected={is_success}')

    # Configure DataUpdateCoordinator
    async def f():
        return await hass.async_add_executor_job(data_updater(inverter))
    coordinator = DataUpdateCoordinator(
        hass,
        logger,
        name=DOMAIN,
        update_method=f,
        update_interval=max(timedelta(seconds=config_entry.data.get(CONF_SCAN_INTERVAL, 60)),
                            MIN_TIME_BETWEEN_UPDATES),
    )

    # Fetch data (at least) once via DataUpdateCoordinator
    await coordinator.async_refresh()
    unique_device_id, inverter_model = _require_device_identity(
        coordinator.data, unique_device_id
    )

    # Register our inverter device
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(DOMAIN, unique_device_id)},
        manufacturer="Sungrow",
        name=f'Sungrow {inverter_model}',
        model=inverter_model
    )

    # Register our sensor entities
    entities = []
    for DESCRIPTION in SENSOR_TYPES:
        # Create a copy, so we don't modify SENSOR_TYPES in place.
        # We cannot have different Sensors use the same SensorEntityDescription.
        description = dataclasses.replace(DESCRIPTION)

        # Add in the owning device's unique id
        description.device_id = unique_device_id
        description.device_model = inverter_model
        model_slug = description.device_model.replace('.', '')
        description.name = f'{model_slug} {unique_device_id} {description.original_name}'
        entities.append(SungrowInverterSensorEntity(coordinator, description))
    async_add_entities(entities, update_before_add=True)


class SungrowInverterSensorEntity(CoordinatorEntity, SensorEntity):
    """Implementation of a Sungrow Inverter sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator,
                 description: SungrowInverterSensorEntityDescription):
        """Initialize the sensor."""
        super().__init__(coordinator)
        # SensorEntity superclass will automatically pull sensor values from entity_description
        self.entity_description = description

    @property
    def unique_id(self) -> str:
        if self._attr_unique_id:
            return self._attr_unique_id
        else:
            self._attr_unique_id = f'sungrow_{self.entity_description.device_id}_{self.entity_description.key}'
            return self._attr_unique_id

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information about this IPP device."""
        if not self.entity_description.device_id:
            return None
        return DeviceInfo(
            identifiers={(DOMAIN, self.entity_description.device_id)},
            name=f'Sungrow {self.entity_description.device_model} {self.entity_description.device_id}',
            manufacturer='Sungrow',
            model=self.entity_description.device_model,
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        sensor_type = self.entity_description.key
        state = None
        try:
            if sensor_type == SUNGROW_ENERGY_GENERATION:
                state = self.coordinator.data.latest_scrape["total_dc_power"]
            elif sensor_type == SUNGROW_ARRAY1_ENERGY_GENERATION:
                state = (
                    self.coordinator.data.latest_scrape["mppt_1_voltage"]
                    * self.coordinator.data.latest_scrape["mppt_1_current"]
                )
            elif sensor_type == SUNGROW_ARRAY2_ENERGY_GENERATION:
                state = (
                    self.coordinator.data.latest_scrape["mppt_2_voltage"]
                    * self.coordinator.data.latest_scrape["mppt_2_current"]
                )
            else:
                state = self.coordinator.data.latest_scrape[sensor_type]
        except KeyError:
            logger.debug(
                "Sensor lookup value is not available in data array: %s", sensor_type)
        if state:
            logger.debug(f'Sensor {sensor_type} value is {state}')
        return state
