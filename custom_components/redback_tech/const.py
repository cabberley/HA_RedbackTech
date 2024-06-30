"""Constants for the redback integration."""

from enum import StrEnum
from datetime import timedelta
import logging
from homeassistant.const import Platform

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
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CALENDAR,
    Platform.DATETIME,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.TEXT,
]


class CronPatterns(StrEnum):
    """Cron patterns."""
    EVERY_MINUTE = "* * * * *"
    EVERY_5_MINUTES = "*/5 * * * *"
    EVERY_30_MINUTES = "*/30 * * * *"
    EVERY_HOUR = "0 * * * *"
    EVERY_DAY = "0 0 * * *"
    EVERY_MONTH = "0 0 1 * *"
    EVERY_YEAR = "0 0 1 1 *"


INVERTER_MODES = [
    "NoMode",
    "Auto",
    "ChargeBattery",
    "DischargeBattery",
    "ImportPower",
    "ExportPower",
    "Conserve",
    "Offgrid",
    "Hibernate",
    "BuyPower",
    "SellPower",
    "ForceChargeBattery",
    "ForceDischargeBattery",
    "Stop",
]
INVERTER_MODES_OPTIONS = [
    "Auto",
    "ChargeBattery",
    "DischargeBattery",
    "ImportPower",
    "ExportPower",
    "Conserve",
    "Offgrid",
    "Hibernate",
    "BuyPower",
    "SellPower",
    "ForceChargeBattery",
    "ForceDischargeBattery",
]

INVERTER_PORTAL_MODES = [
    "Auto",
    "ChargeBattery",
    "DischargeBattery",
    "ImportPower",
    "ExportPower",
    "Conserve",
]

INVERTER_STATUS = ["OK", "Offline", "Fault"]
FAN_STATE = ["Off", "On", "Error"]
