import asyncio
import logging
import json
from datetime import timedelta
import aiohttp

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import DOMAIN
from .const import SENSOR, APIKEY, CODE

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Hibouair platform."""
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Hibouair Sensor",
        update_method=async_update_data,
        update_interval=timedelta(minutes=10),
    )

    await coordinator.async_refresh()
    api_key = hass.data[DOMAIN]["api_key"]
    code = hass.data[DOMAIN]["code"]

    async_add_entities(
        [
            HibouairSensor(coordinator, api_key, code),
            HibouairSensor(
                coordinator, "temperature", "Temperature", "°C", "mdi:thermometer"
            ),
            HibouairSensor(
                coordinator, "humidity", "Humidity", "%rH", "mdi:water-percent"
            ),
            HibouairSensor(coordinator, "pm1", "PM1", "µg/m³", "mdi:blur"),
            HibouairSensor(coordinator, "pm25", "PM2.5", "µg/m³", "mdi:blur"),
            HibouairSensor(coordinator, "pm10", "PM10", "µg/m³", "mdi:blur"),
            HibouairSensor(coordinator, "voc", "VOC", "ppm", "mdi:cloud"),
            HibouairSensor(coordinator, "co2", "CO2", "ppm", "mdi:molecule-co2"),
            HibouairSensor(coordinator, "pressure", "Pressure", "mbar", "mdi:gauge"),
            HibouairSensor(coordinator, "ts", "Last updated", "", "mdi:calendar-clock"),
            HibouairSensor(coordinator, "als", "Light", "lux", "mdi:brightness-7"),
        ]
    )


async def async_update_data():
    """Fetch data from your data source and return it."""
    try:
        url = f"https://www.hibouconnect.com/tapi/current"
        headers = {
            "sensor": SENSOR,
            "api-key": api_key,
            "code": code,
            #'app': 'hibou5775',
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.text()
                parsed_data = json.loads(data)
                temperature = parsed_data.get("t")
                humidity = parsed_data.get("h")
                pm1 = parsed_data.get("pm1")
                pm25 = parsed_data.get("pm25")
                pm10 = parsed_data.get("pm10")
                voc = parsed_data.get("voc")
                co2 = parsed_data.get("co2")
                pressure = parsed_data.get("p")
                als = parsed_data.get("als")
                ts = parsed_data.get("ts")
                _LOGGER.error("API here %s", parsed_data)

                return {
                    "temperature": temperature,
                    "humidity": humidity,
                    "pm1": pm1,
                    "pm25": pm25,
                    "pm10": pm10,
                    "voc": voc,
                    "co2": co2,
                    "als": als,
                    "pressure": pressure,
                    "ts": ts,
                }

    except Exception as e:
        _LOGGER.error("Error updating HibouAir sensor: %s", e)
    # Replace with your actual data retrieval logic
    # return {
    #     'temperature': 25.5,
    #     'humidity': 50.0,
    #     'pm1': 10,
    #     'pm25': 25,
    #     'pm10': 50,
    #     'voc': 300,
    #     'co2': 500,
    #     'als': 200
    # }


class HibouairSensor(Entity):
    """Representation of a Hibouair sensor."""

    def __init__(
        self, coordinator, sensor_type, sensor_name, unit, icon, api_key, code
    ):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._api_key = api_key
        self._code = code
        self._sensor_type = sensor_type
        self._sensor_name = sensor_name
        self._unit = unit
        self._icon = icon

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Hibouair {self._sensor_name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        data = self._coordinator.data
        return data.get(self._sensor_type)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def icon(self):
        """Return the icon to be displayed for this entity."""
        return self._icon

    async def async_update(self):
        """Update the sensor."""
        await self._coordinator.async_request_refresh()
