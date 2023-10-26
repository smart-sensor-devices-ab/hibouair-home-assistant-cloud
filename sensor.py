import asyncio
import logging
import json
from datetime import timedelta
import aiohttp

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_PRESSURE, DEVICE_CLASS_ILLUMINANCE, DEVICE_CLASS_CO2, TEMP_CELSIUS, PERCENTAGE, PRESSURE_HPA, CONCENTRATION_PARTS_PER_MILLION
from homeassistant.helpers.entity import Entity

from .const import NAME, SENSOR,APIKEY,CODE,DEFAULT_SCAN_INTERVAL,INTERVAL

_LOGGER = logging.getLogger('hibouair')

DEFAULT_NAME = "HibouAir"
DEFAULT_INTERVAL = timedelta(minutes=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(INTERVAL, default=DEFAULT_INTERVAL): cv.time_period,
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    name = NAME
    sensor_id = SENSOR
    api_key = APIKEY
    code = CODE
    interval = INTERVAL

    sensors = []
    
    for attribute in ['p', 't', 'h', 'voc', 'als', 'pm1', 'pm25', 'pm10', 'co2', 'ts']:
        sensor = HibouAirSensor(hass, name, sensor_id, api_key,code, interval, attribute)
        sensors.append(sensor)
    
    async_add_entities(sensors, update_before_add=True)

class HibouAirSensor(Entity):
    def __init__(self, hass, name, sensor_id, api_key,code, interval, attribute):
        self._hass = hass
        self._name = f"{name} {attribute}"
        self._sensor_id = sensor_id
        self._api_key = api_key
        self._code = code
        self._state = None
        self._attribute = attribute
        self._unit = None
        self._device_class = None
        self._interval = interval

        if attribute == 'p':
            self._name = "HibouAir Pressure"
            self._unit = PRESSURE_HPA
            self._device_class = DEVICE_CLASS_PRESSURE
            self._friendly_name="Pressure"
        elif attribute == 't':
            self._name = "HibouAir Temperature"
            self._unit = TEMP_CELSIUS
            self._device_class = DEVICE_CLASS_TEMPERATURE
            self._friendly_name="Temperature"
        elif attribute == 'h':
            self._name = "HibouAir Humidity"
            self._unit = PERCENTAGE
            self._device_class = DEVICE_CLASS_HUMIDITY
            self._friendly_name="Humidity"
        elif attribute == 'als':
            self._name = "HibouAir Light"
            self._unit = 'lux'
            self._device_class = DEVICE_CLASS_ILLUMINANCE
            self._friendly_name="Light"
        elif attribute == 'co2':
            self._name = "HibouAir CO2"
            self._unit = CONCENTRATION_PARTS_PER_MILLION
            self._device_class = DEVICE_CLASS_CO2
            self._friendly_name="CO2"
        elif attribute == 'ts':
            self._name = "HibouAir Last Update"
            self._icon = "mdi:clock"
            self._friendly_name="Last Update"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state
    
    @property
    def device_class(self):
        return self._device_class

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def device_state_attributes(self):
        return self._attributes

    async def async_update(self):
        try:
            url = f"https://www.hibouconnect.com/tapi/current"
            headers = {
                'sensor': self._sensor_id,
                'api-key': self._api_key,
                'code': self._code,
                'app': 'hibou5775',
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    data = await response.text()
                    parsed_data = json.loads(data)
                    self._state = parsed_data.get(self._attribute)

        except Exception as e:
            _LOGGER.error("Error updating HibouAir sensor: %s", e)
                
