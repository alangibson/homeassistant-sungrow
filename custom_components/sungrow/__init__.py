"""Sungrow Inverter integration."""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

logger = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Entry point to set up Sungrow Inverter"""
    # Forward the setup to the sensor platform.
    return await hass.config_entries.async_forward_entry_setup(config_entry, Platform.SENSOR)


# TODO Unload gracefully
# https://github.com/home-assistant/core/blob/dev/homeassistant/components/fronius/__init__.py
# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Unload a config entry."""
#     unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
#     if unload_ok:
#         solar_net = hass.data[DOMAIN].pop(entry.entry_id)
#         while solar_net.cleanup_callbacks:
#             solar_net.cleanup_callbacks.pop()()
#     return unload_ok