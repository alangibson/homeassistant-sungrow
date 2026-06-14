# Sungrow inverter integration for Home Assistant

## Installation

Make sure your Sungrow inverter firmware is up to date. You can find the latest firmware here:
https://github.com/sungrow-firmware/firmware

This guide assumes you already have HACS installed.

- Add repository https://github.com/alangibson/homeassistant-sungrow as an Integration repo in HACS Custom Repositories menu
- Add Sungrow repository in HACS
- Download the Integration in HACS
- Restart Home Assistant

## Configuration

- Add the Sungrow integration in the HA Devices and Services menu
- When prompted, enter the IP address or hostname of your inverter
  - You can probably leave everything else at the defaults

## Development

### Prepare Environment

```
python3 -m venv venv
./venv/bin/pip install homeassistant pymodbus==3.11.3
```

Then follow these instructions to set your VS Code python interpreter to use ./venv

https://code.visualstudio.com/docs/python/environments

### Running

To test locally, the  run

```
docker compose up
```

and open http://localhost:8123 in your browser.
