"""Sensor platform for Redback Tech integration."""

from __future__ import annotations

from typing import Any

from redbacktechpy.model import Inverters

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REDBACKTECH_COORDINATOR, REDBACK_PORTAL, MANUFACTURER, LOGGER
from .coordinator import RedbackTechDataUpdateCoordinator
from .sensor_properties import (
    ENTITY_DETAILS,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Redback Tech Sensor Entities."""
    global redback_devices, redback_entity_details, redback_dataSet

    coordinator: RedbackTechDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        REDBACKTECH_COORDINATOR
    ]
    redback_devices = coordinator.data.devices
    redback_entity_details = coordinator.data.entities
    sensors = []
    redback_dataSet = "entities"
    entity_keys = coordinator.data.entities.keys()
    for entity_key in entity_keys:
        if entity_key[7:] in ENTITY_DETAILS:
            sensors.extend([RedbackTechSensorEntity(coordinator, entity_key)])
    async_add_entities(sensors)

class RedbackTechSensorEntity(CoordinatorEntity, SensorEntity):
    """Representation of a Redback Tech Sensor Entity."""

    def __init__(self, coordinator, entity_key):
        super().__init__(coordinator)
        self.ent_id = entity_key[:7]
        self.ent_key = entity_key
        self.entity_id = (
            "sensor.rb"
            + self.ent_id[:4]
            + "_"
            + self.ent_id[-3:].lower().replace(" ", "_")
            + "_"
            + ENTITY_DETAILS[self.ent_key[7:]]["name"].lower().replace(" ", "_")
        )

    @property
    def ent_data(self) -> Inverters:
        """Handle coordinator data for entities."""
        return self.coordinator.data.entities[self.ent_key]

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device registry information for this entity."""
        return {
            "identifiers": {(DOMAIN, redback_devices[self.ent_id].identifiers)},
            "name": redback_devices[self.ent_id].name,
            "manufacturer": MANUFACTURER,
            "model": redback_devices[self.ent_id].model,
            "sw_version": redback_devices[self.ent_id].sw_version,
            "hw_version": redback_devices[self.ent_id].hw_version,
            "serial_number": redback_devices[self.ent_id].serial_number,
            "configuration_url": REDBACK_PORTAL,
        }

    @property
    def unique_id(self) -> str:
        """Sets unique ID for this entity."""
        return self.ent_key

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return False

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return ENTITY_DETAILS[self.ent_key[7:]]["name"]

    @property
    def native_value(self) -> float:
        """Return the state of the entity."""
        return self.ent_data.data["value"]

    @property
    def entity_registry_visible_default(self) -> bool:
        """Return whether the entity should be visible by default."""
        if ENTITY_DETAILS[self.ent_key[7:]]["visible"]:
            return True
        elif self.ent_data.data["value"] is None:
            return False
        return True

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return whether the entity should be enabled by default."""
        if ENTITY_DETAILS[self.ent_key[7:]]["enabled"]:
            return True
        elif self.ent_data.data["value"] is None:
            return False
        return True

    @property
    def native_unit_of_measurement(self):
        """Return native Unit of Measurement for this entity."""
        if ENTITY_DETAILS[self.ent_key[7:]]["unit"] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]["unit"]
        return

    @property
    def device_class(self) -> SensorDeviceClass:
        """Return entity device class."""
        if ENTITY_DETAILS[self.ent_key[7:]]["device_class"] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]["device_class"]
        return

    @property
    def suggested_display_precision(self) -> int:
        """Return the suggested precision for the value."""
        if ENTITY_DETAILS[self.ent_key[7:]]["display_precision"] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]["display_precision"]  # 3
        return

    @property
    def state_class(self) -> SensorStateClass:
        """Return the type of state class."""
        if ENTITY_DETAILS[self.ent_key[7:]]["state_class"] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]["state_class"]
        return

    @property
    def entity_category(self) -> EntityCategory:
        """Set category to diagnostic."""
        if ENTITY_DETAILS[self.ent_key[7:]]["category"] is not None:
            return EntityCategory.DIAGNOSTIC
        return
