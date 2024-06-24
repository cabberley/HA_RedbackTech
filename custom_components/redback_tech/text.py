"""Sensor platform for Redback Tech integration."""

from __future__ import annotations
from typing import Any

from redbacktechpy.model import Numbers

from homeassistant.components.text import (
    TextEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REDBACKTECH_COORDINATOR, REDBACK_PORTAL, MANUFACTURER, LOGGER
from .coordinator import RedbackTechDataUpdateCoordinator
from .text_properties import ENTITY_DETAILS


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Redback Tech Sensor Entities."""
    global redback_devices, redback_entity_details

    coordinator: RedbackTechDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        REDBACKTECH_COORDINATOR
    ]

    redback_devices = coordinator.data.devices
    redback_entity_details = coordinator.data.entities
    numbers = []

    entity_keys = coordinator.data.text.keys()
    for entity_key in entity_keys:
        if entity_key[7:] in ENTITY_DETAILS:
            numbers.extend([RedbackTechTextEntity(coordinator, entity_key)])

    async_add_entities(numbers)


class RedbackTechTextEntity(CoordinatorEntity, TextEntity):
    """Representation of Number."""

    def __init__(self, coordinator, entity_key):
        super().__init__(coordinator)
        self.ent_id = entity_key[:7]
        self.ent_key = entity_key
        self.entity_id = (
            "text.rb"
            + self.ent_id[:4]
            + "_"
            + self.ent_id[-3:].lower()
            + "_"
            + ENTITY_DETAILS[self.ent_key[7:]]["name"]
        )
        LOGGER.debug("text_data1: %s", self.ent_data)
        LOGGER.debug("text_ent_id: %s", self.ent_id)

    @property
    def ent_data(self) -> Numbers:
        """Handle coordinator data for entities."""
        return self.coordinator.data.text[self.ent_key]

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
    def icon(self) -> str:
        """Set icon for this entity, if provided in parameters."""
        if ENTITY_DETAILS[self.ent_key[7:]]["icon"] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]["icon"]
        return

    @property
    def entity_registry_visible_default(self) -> bool:
        """Return whether the entity should be visible by default."""
        return True

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return whether the entity should be enabled by default."""
        return True

    @property
    def native_value(self) -> float:
        """Return the state of the entity."""
        LOGGER.debug("native Value : %s", self.ent_data.data["value"])
        value = self.ent_data.data["value"]
        return value

    @property
    def mode(self):
        """Return box mode."""

        return "text"

    @property
    def native_min(self) -> float:
        """Return minimum allowed value."""
        if ENTITY_DETAILS[self.ent_key[7:]]["native_min"] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]["native_min"]
        pass

    @property
    def native_max(self) -> float:
        """Return minimum allowed value."""
        if ENTITY_DETAILS[self.ent_key[7:]]["native_max"] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]["native_max"]
        return

    async def async_set_value(self, value: str) -> None:
        """Update the current value."""
        self.ent_data.data["value"] = value
        LOGGER.debug("ent_data_value updated: %s", self.ent_data.data["value"])
        if self.ent_data.data["entity_name"] == "op_env_create_event_id":
            LOGGER.debug("max_import")
            await self.coordinator.client.update_op_envelope_values(
                self.ent_data.data["device_id"], "EventId", value
            )

        self.async_write_ha_state()
        # await self.coordinator.async_request_refresh()
