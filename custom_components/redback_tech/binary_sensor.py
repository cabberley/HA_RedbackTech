"""Sensor platform for Redback Tech integration."""
from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
     BinarySensorEntity
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
    LOGGER,
)
from .coordinator import RedbackTechDataUpdateCoordinator
from .binary_sensor_inverter_properties import (
    ENTITY_DETAILS
)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set Up Redback Tech Sensor Entities."""
    global redback_devices, redback_entity_details
    
    coordinator: RedbackTechDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][REDBACKTECH_COORDINATOR]

    redback_devices = coordinator.data.devices    
    redback_entity_details = coordinator.data.entities
    binary_sensors = []

    entity_keys = coordinator.data.entities.keys()
    #swap this around to get the binary sensors quicker
    for entity_key in entity_keys:
        if entity_key[7:] in  ENTITY_DETAILS: 
            binary_sensors.extend([RedbackTechBinarySensorEntity(coordinator, entity_key)])
    
    async_add_entities(binary_sensors)
    
class RedbackTechBinarySensorEntity(CoordinatorEntity, BinarySensorEntity):
    """Representation of Binary Sensor."""

    def __init__(self, coordinator, entity_key):
        super().__init__(coordinator)
        self.ent_id = entity_key[:7]
        self.ent_key = entity_key
        self.entity_id = 'number.rb'+self.ent_id[:4] + '_' + self.ent_id[-3:].lower() + '_' + ENTITY_DETAILS[self.ent_key[7:]]['name']
        LOGGER.debug(f'number_data1: {self.ent_data}')
        LOGGER.debug(f'number_data2: {self.ent_id}')

    @property
    def ent_data(self):
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
    def entity_registry_visible_default(self) -> bool:
        """Return whether the entity should be visible by default."""
        if ENTITY_DETAILS[self.ent_key[7:]]['visible']:
            return True
        elif self.ent_data.data['value'] is None:
            return False    
        return True
    
    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return whether the entity should be enabled by default."""
        if ENTITY_DETAILS[self.ent_key[7:]]['enabled']:
            return True
        elif self.ent_data.data['value'] is None:
            return False    
        return True

    @property
    def is_on(self) -> bool:
        """Return the state of the entity."""
        value = self.ent_data.data['value']
        if value:
            return True
        return False
    
    async def reset_to_auto(self) -> None:
        """Update the current value."""
        await self.coordinator.client.reset_inverter_to_auto( self.ent_id)
        
    async def create_schedule_event(self, power_mode,power_setting,duration,start_time):
        """Update the current value."""
        await self.coordinator.client.create_schedule_event( self.ent_id, power_setting_mode= power_mode, power_setting_watts = power_setting, power_setting_duration = duration, start_time = start_time)