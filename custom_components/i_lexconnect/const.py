import logging
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfTime, UnitOfVolume

DOMAIN = "i_lexconnect"

UPDATE_INTERVAL = timedelta(minutes=5)
API_TIMEOUT = 20

LOGGER = logging.getLogger(__package__)

API_CS1    = "getCS1"            # water reserve percent
API_RES    = "getRES"            # water reserve in liters
API_IWH    = "getIWH"            # incoming water hardness (°fH)
API_OWH    = "getOWH"            # outgoing water hardness (°fH)
API_SD1    = "getSD1"            # salt reserve in days
API_TOR    = "getTOR"            # total number of regenerations
API_MAC    = "getMAC"            # MAC address
API_FW     = "firmware"          # firmware type
API_VER    = "getVER"            # firmware version
API_DTYPE  = "dtype"             # device type
API_STATUS = "status"            # online status
API_SRN    = "getSRN"            # serial number
API_DATE   = "getDATasTimestamp" # date of live data

UNIT_WATER_HARDNESS = "°fH"

SENSOR_TYPES = (
    SensorEntityDescription(
        key=API_CS1,
        native_unit_of_measurement=PERCENTAGE,
        name="Water reserve",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_RES,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        name="Water reserve volume",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_IWH,
        native_unit_of_measurement=UNIT_WATER_HARDNESS,
        name="Incoming water hardness",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_OWH,
        native_unit_of_measurement=UNIT_WATER_HARDNESS,
        name="Outgoing water hardness",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_SD1,
        native_unit_of_measurement=UnitOfTime.DAYS,
        name="Salt reserve",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_TOR,
        name="Total regenerations",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_DATE,
        name="Last update",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
)