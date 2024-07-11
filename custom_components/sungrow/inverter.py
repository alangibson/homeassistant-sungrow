from pprint import pformat
import pathlib, yaml, os, logging
from typing import Tuple

from homeassistant.helpers.update_coordinator import (
    UpdateFailed
)

from .SunGather.inverter import SungrowInverter

logger = logging.getLogger(__name__)


def create_inverter(config_inverter: dict) -> SungrowInverter:
    def f():
        pwd = pathlib.Path(__file__).parent.absolute()
        registersfile = yaml.safe_load(
            open(os.path.join(pwd, 'registers-sungrow.yaml'), encoding="utf-8"))
        inverter = SungrowInverter(config_inverter)
        if not inverter.checkConnection():
            # logger.error(
            #     f"Error: Connection to inverter failed: {config_inverter.get('host')}:{config_inverter.get('port')}")
            raise Exception(f"Error: Connection to inverter failed: {config_inverter.get('host')}:{config_inverter.get('port')}")
        inverter.configure_registers(registersfile)
        # if not inverter.inverter_config['connection'] == "http":
        #     inverter.close()
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
        inverter.scrape()
        logger.debug(
            f'async_update_data latest_scrape={pformat(inverter.latest_scrape)}')
        if inverter.latest_scrape == {}:
            raise UpdateFailed(f"Failed scraping Sungrow Inverter")
        return inverter
    return u
