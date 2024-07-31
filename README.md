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

To test locally, just run

```
docker-compose up
```

and open http://localhost:8123 in your browser.



## Flows

### Setup Flow

config_flow.async_step_user
    config_flow._async_show_user_form
config_flow.async_step_user
    config_flow.validate_input
        async_add_executor_job
            inverter.connect_inverter
                inverter.create_inverter
                inverter.scrape

