from pprint import pformat
import pathlib, yaml, logging
from typing import Tuple

from homeassistant.helpers.update_coordinator import (
    UpdateFailed
)

from .SunGather.inverter import SungrowInverter

logger = logging.getLogger(__name__)


def create_inverter(config_inverter: dict) -> SungrowInverter:
    def f():
        pwd = pathlib.Path(__file__).parent.absolute()
        with open(pwd / 'registers-sungrow.yaml', encoding="utf-8") as register_file:
            registersfile = yaml.safe_load(register_file)
        inverter = SungrowInverter(config_inverter)
        if not inverter.checkConnection():
            # logger.error(
            #     f"Error: Connection to inverter failed: {config_inverter.get('host')}:{config_inverter.get('port')}")
            failure_reason = (
                inverter.last_register_read_failure or "client connection failed"
            )
            raise Exception(
                f"Error: Connection to inverter failed: {config_inverter.get('host')}:{config_inverter.get('port')}: {failure_reason}"
            )
        inverter.configure_registers(registersfile)
        # Monitoring only: control/settings holding registers are not needed by
        # HA sensors and some WiNet firmware rejects reads of these registers.
        inverter.registers = [r for r in inverter.registers if r["type"] == "read"]
        if inverter.getInverterModel().startswith("SG") and not config_inverter.get("smart_meter"):
            meter_registers = {
                "power_meter", "export_power", "load_power",
                "daily_export_energy", "total_export_energy",
                "daily_import_energy", "total_import_energy",
                "daily_direct_energy_consumption", "total_direct_energy_consumption",
            }
            inverter.registers = [r for r in inverter.registers
                                  if not r.get("smart_meter")
                                  and not r["name"].startswith("meter_")
                                  and r["name"] not in meter_registers]
        inverter.register_ranges = [
            block for block in inverter.register_ranges if block["type"] == "read"
            and any(block["start"] <= r["address"] - 1
                    and r["address"] - 1 + inverter._get_register_count(r)
                    <= block["start"] + block["range"]
                    for r in inverter.registers)
        ]
        return inverter
    return f


def connect_inverter(config_inverter: dict) -> Tuple[bool, SungrowInverter]:
    def f():
        inverter = create_inverter(config_inverter)()
        is_success = inverter.scrape()
        return is_success, inverter
    return f


def data_updater(inverter: SungrowInverter):
    """Function called by DataUpdateCoordinator to do the data refresh from the inverter"""
    def u():
        logger.debug(f'async_update_data scrape inverter={inverter}')
        is_connected = inverter.connect()
        logger.debug(f'async_update_data is_connected={is_connected}')
        if not is_connected or not inverter.scrape():
            raise UpdateFailed(inverter.last_register_read_failure or "Failed scraping Sungrow inverter")
        logger.debug(
            f'async_update_data latest_scrape={pformat(inverter.latest_scrape)}')
        if inverter.latest_scrape == {}:
            raise UpdateFailed(f"Failed scraping Sungrow Inverter")
        return inverter
    return u
