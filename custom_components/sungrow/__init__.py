"""
Sungrow Inverter integration.

This module is the glue that allows HA to start this integration.
"""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry, ConfigEntryNotReady
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SLAVE,
    CONF_TIMEOUT,
    Platform,
)
from homeassistant.helpers import issue_registry as ir

from .const import DEFAULT_SLAVE, DOMAIN
from .inverter import connect_inverter

logger = logging.getLogger(__name__)
IDENTITY_ISSUE_KEY = "missing_device_identity"


def _get_failure_reason(inverter) -> str | None:
    """Return the last recorded inverter failure reason."""
    if not inverter:
        return None
    return getattr(inverter, "last_register_read_failure", None)


def _get_identity_failure_reason(
    serial_number: str | None,
    model: str | None,
    failure_reason: str | None,
) -> str:
    """Return a user-readable reason for incomplete device identity."""
    if failure_reason:
        return failure_reason

    missing = []
    if not serial_number:
        missing.append("serial number")
    if not model:
        missing.append("model")

    if missing:
        return (
            f"missing {' and '.join(missing)}; "
            f"serial_number={serial_number or 'missing'}, model={model or 'missing'}"
        )

    return "device identity validation failed"


def _identity_issue_id(config_entry: ConfigEntry) -> str:
    """Return the repair issue id for a config entry."""
    return f"{IDENTITY_ISSUE_KEY}_{config_entry.entry_id}"


def _show_identity_issue(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    *,
    serial_number: str | None,
    model: str | None,
    reason: str | None,
) -> None:
    """Create or update a visible repair issue for missing identity."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        _identity_issue_id(config_entry),
        is_fixable=False,
        is_persistent=True,
        severity=ir.IssueSeverity.ERROR,
        translation_key=IDENTITY_ISSUE_KEY,
        translation_placeholders={
            "host": str(config_entry.data.get(CONF_HOST)),
            "serial_number": str(serial_number or "missing"),
            "model": str(model or "missing"),
            "reason": str(reason or "unknown"),
        },
    )


def _clear_identity_issue(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Clear the visible repair issue after identity validation succeeds."""
    ir.async_delete_issue(hass, DOMAIN, _identity_issue_id(config_entry))


def _migrate_legacy_connection_options(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Remove legacy connection options from config entry data."""
    if "connection" not in config_entry.data:
        return

    data = dict(config_entry.data)
    connection = data.pop("connection")

    if connection in ("http", "sungrow"):
        data[CONF_PORT] = 502
    else:
        data.setdefault(CONF_PORT, 502)

    hass.config_entries.async_update_entry(config_entry, data=data)


def _build_inverter_config(config_entry: ConfigEntry) -> dict:
    """Build the inverter connection config from a config entry."""
    return {
        "host": config_entry.data[CONF_HOST],
        "port": config_entry.data.get(CONF_PORT, "502"),
        "timeout": int(config_entry.data.get(CONF_TIMEOUT, 10)),
        "retries": 3,
        "slave": config_entry.data.get(CONF_SLAVE, DEFAULT_SLAVE),
        "serial_number": config_entry.data.get("serial_number"),
        "model": config_entry.data.get("model"),
        "level": config_entry.data.get("level", 2),
        "use_local_time": config_entry.data.get("use_local_time", False),
        "smart_meter": config_entry.data.get("smart_meter"),
        "use_scan_ranges": config_entry.data.get("use_scan_ranges", False),
    }


def _get_device_identity(config_entry: ConfigEntry, inverter) -> tuple[str | None, str | None]:
    """Get serial number and model from config entry or inverter data."""
    serial_number = (
        config_entry.data.get("device_id")
        or config_entry.data.get("serial_number")
        or inverter.latest_scrape.get("serial_number")
    )
    model = inverter.getInverterModel()
    return serial_number, model


async def _ensure_device_identity(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Validate identity before forwarding setup to sensor platform."""
    try:
        is_success, inverter = await hass.async_add_executor_job(
            connect_inverter(_build_inverter_config(config_entry))
        )
    except Exception as err:
        _show_identity_issue(
            hass,
            config_entry,
            serial_number=None,
            model=config_entry.data.get("model"),
            reason=str(err),
        )
        logger.error(
            "Sungrow inverter setup failed before sensor creation "
            "(host=%s): %s",
            config_entry.data.get(CONF_HOST),
            err,
        )
        raise ConfigEntryNotReady(f"Sungrow inverter is not ready: {err}") from err

    logger.debug("Sungrow preflight connection is_success=%s", is_success)

    serial_number, model = _get_device_identity(config_entry, inverter)
    if serial_number and model:
        if not is_success:
            logger.warning(
                "Sungrow inverter setup continuing after failed register reads "
                "(serial_number=%s, model=%s, host=%s, reason=%s)",
                serial_number,
                model,
                inverter.getHost() if inverter else config_entry.data.get(CONF_HOST),
                _get_failure_reason(inverter),
            )
        data = dict(config_entry.data)
        if data.get("device_id") != serial_number:
            data["device_id"] = serial_number
        if not data.get("model"):
            data["model"] = model
        if data != config_entry.data:
            hass.config_entries.async_update_entry(config_entry, data=data)
        _clear_identity_issue(hass, config_entry)
        return

    failure_reason = _get_identity_failure_reason(
        serial_number, model, _get_failure_reason(inverter)
    )
    _show_identity_issue(
        hass,
        config_entry,
        serial_number=serial_number,
        model=model,
        reason=failure_reason,
    )
    logger.error(
        "Sungrow inverter setup failed: missing required device identity before "
        "sensor creation (serial_number=%s, model=%s, host=%s, reason=%s)",
        serial_number,
        model,
        inverter.getHost() if inverter else config_entry.data.get(CONF_HOST),
        failure_reason,
    )
    raise ConfigEntryNotReady(
        "Sungrow inverter did not report both serial number and model: "
        f"{failure_reason}"
    )


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Entry point to set up Sungrow Inverter"""
    _migrate_legacy_connection_options(hass, config_entry)
    await _ensure_device_identity(hass, config_entry)

    # Forward the setup to the sensor platform.
    await hass.config_entries.async_forward_entry_setups(config_entry, [Platform.SENSOR])
    return True


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
