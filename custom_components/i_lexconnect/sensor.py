from homeassistant.util import dt
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    LOGGER,
    SENSOR_TYPES,
    API_MAC,
    API_FW,
    API_VER,
    API_DTYPE,
    API_STATUS,
    API_SD1,
    API_SS1,
    API_TOR,
    API_DATE
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []

    for serial, data in coordinator.data.items():
        device_sensors = data.keys()
        entities.extend(
            [
                ILexSensor(serial, coordinator, description)
                for description in SENSOR_TYPES
                if description.key in device_sensors
            ]
        )

    async_add_entities(entities)


class ILexSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, serial, coordinator, description):
        """Set up an individual I-LexConnect sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._serial = serial

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._serial} {self.entity_description.name}"

    @property
    def unique_id(self):
        """Return the uuid as the unique_id."""
        return f"{self._serial.lower()}_{self.entity_description.key.lower()}"

    @property
    def available(self):
        """Determine if the sensor is available based on API results."""
        # If the last update was successful...
        if self.coordinator.last_update_success and self._data:
            # and the results included our sensor type...
            sensor_type = self.entity_description.key
            if "online" == self._data[API_STATUS].lower():
                # then we are available.
                return True

        # Otherwise, we are not.
        return False

    @property
    def native_value(self):
        """Return the state, rounding off to reasonable values."""
        if not self._data:
            return None

        sensor_type = self.entity_description.key
        state = None
        value = self._data[sensor_type]
        if sensor_type in [API_SD1, API_SS1, API_TOR]:
            state = int(value)
        elif sensor_type == API_DATE:
            state = dt.utc_from_timestamp(float(value))
        else:
            state = round(float(value), 2)

        return state


    @property
    def device_info(self):
        """Device information."""
        info = DeviceInfo(
            identifiers={(DOMAIN, self._serial)},
            name=self._serial,
            manufacturer="ILexConnect",
            model=self._data[API_DTYPE],
            sw_version=f"{self._data[API_FW]}.{self._data[API_VER]}",
            connections={
                (dr.CONNECTION_NETWORK_MAC, self._data[API_MAC])
            }
        )

        return info

    @property
    def _data(self):
        """Return the latest data for our device, or None."""
        return self.coordinator.data.get(self._serial)
