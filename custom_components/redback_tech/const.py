"""Constants for the redback integration."""

from homeassistant.const import Platform
from datetime import timedelta
import logging

LOGGER = logging.getLogger(__package__)

DOMAIN = "redback_tech"
DEFAULT_NAME = "RedbackTechnologies"
POLLING_INTERVAL = "polling_interval"
UPDATE_LISTENER = "update_listener"
SCAN_INTERVAL = 60
TIMEOUT = 20
LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(minutes=1)
REDBACKTECH_COORDINATOR = "redbacktech_coordinator"
REDBACK_PORTAL = "https://portal.redbacktech.com"
MANUFACTURER = "Redback Technologies"
PLATFORMS = [
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.DATETIME,
    Platform.BUTTON,
]

INVERTER_MODES = ["NoMode", "Auto", "ChargeBattery", "DischargeBattery", "ImportPower", "ExportPower", "Conserve", "Offgrid", "Hibernate", "BuyPower", "SellPower", "ForceChargeBattery", "ForceDischargeBattery", "Stop"]
INVERTER_MODES_OPTIONS = ["Auto", "ChargeBattery", "DischargeBattery", "ImportPower", "ExportPower", "Conserve"]
INVERTER_STATUS = ["OK", "Offline", "Fault"]
FAN_STATE = ["Off", "On", "Error"]

