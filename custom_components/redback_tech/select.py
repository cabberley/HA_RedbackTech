"""Sensor platform for Redback Tech integration."""
from __future__ import annotations

from datetime import datetime, timezone
from math import floor as floor
from typing import Any

from redbacktechpy.model import Numbers

from homeassistant.components.select import (
    
    SelectEntity,

)
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    REDBACKTECH_COORDINATOR,
    REDBACK_PORTAL,
    MANUFACTURER,
    LOGGER

)
from .coordinator import RedbackTechDataUpdateCoordinator
from .select_inverter_properties import (
    ENTITY_DETAILS
)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Redback Tech Sensor Entities."""
    global redback_devices 
    
    coordinator: RedbackTechDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][REDBACKTECH_COORDINATOR]

    redback_devices = coordinator.data.devices    
    
    selects = []

    entity_keys = coordinator.data.selects.keys()
    LOGGER.debug(f'Select Key Match: {entity_keys}')
    for entity_key in entity_keys:
        LOGGER.debug(f'Select Key Match: {entity_key}')
        if entity_key[7:] in  ENTITY_DETAILS: 
            selects.extend([RedbackTechSelectsEntity(coordinator, entity_key)])
    
    async_add_entities(selects)
    
class RedbackTechSelectsEntity(CoordinatorEntity, SelectEntity):
    """Representation of Number."""

    def __init__(self, coordinator, entity_key):
        super().__init__(coordinator)
        self.ent_id = entity_key[:7]
        self.ent_key = entity_key
        self.entity_id = 'select.rb'+self.ent_id[:4] + '_' + self.ent_id[-3:].lower() + '_' + ENTITY_DETAILS[self.ent_key[7:]]['name']
        LOGGER.debug(f'select_data1: {self.ent_data}')
        LOGGER.debug(f'select_data2: {self.ent_id}')
        LOGGER.debug(f'select_data2: {self.entity_id}')

    @property
    def ent_data(self) -> Numbers:
        """Handle coordinator data for entities."""
        LOGGER.debug(f'select_data22: {self.coordinator.data.selects[self.ent_key]}')
        return self.coordinator.data.selects[self.ent_key]

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device registry information for this entity."""
        return {
            "identifiers": {(DOMAIN, redback_devices[self.ent_id].identifiers)},  
            "name": redback_devices[self.ent_id].name, 
            "manufacturer": MANUFACTURER,
            "model": redback_devices[self.ent_id].model,
            "sw_version": redback_devices[self.ent_id].sw_version,
            'hw_version': redback_devices[self.ent_id].hw_version,
            'serial_number': redback_devices[self.ent_id].serial_number,
            'configuration_url':REDBACK_PORTAL
        }

    @property
    def unique_id(self) -> str:
        """Sets unique ID for this entity."""
        return  self.ent_key 

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return False

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return ENTITY_DETAILS[self.ent_key[7:]]['name']

    @property
    def icon(self) -> str:
        """Set icon for this entity, if provided in parameters."""
        if ENTITY_DETAILS[self.ent_key[7:]]['icon'] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]['icon'] 
        pass

    @property
    def current_option(self) -> str:
        """Return the current option."""
        return self.ent_data.data['value']

    @property
    def options(self) -> list[str]:
        """Return the list of available options."""
        LOGGER.debug(f'options_data: {str(self.ent_data.data['options'])}')
        return self.ent_data.data['options'] 

    async def async_select_option(self, option: str) -> None:
        """Update the current value."""
        
        LOGGER.debug(f'number_data: {self.ent_data}')
        LOGGER.debug(f'number_value: {option}')
        if self.ent_key[7:] == 'power_setting_mode':
            await self.coordinator.client.update_inverter_control_values( self.ent_data.data['device_id'], self.ent_data.data['entity_name'], option)
        elif self.ent_key[7:] == 'schedule_id_selected':
            await self.coordinator.client.update_selected_schedule_id( self.ent_data.data['device_id'], option)
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()
