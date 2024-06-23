"""Sensor platform for Redback Tech integration."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from redbacktechpy.model import ScheduleDateTime

from homeassistant.components.datetime import (
    DateTimeEntity,
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
from .datetime_properties import (
    ENTITY_DETAILS
)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Redback Tech Sensor Entities."""
    global redback_devices
    
    coordinator: RedbackTechDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][REDBACKTECH_COORDINATOR]

    redback_devices = coordinator.data.devices    
    datetime_entitys = []

    entity_keys = coordinator.data.schedules_datetime_data.keys()
    for entity_key in entity_keys:
        if entity_key[7:] in  ENTITY_DETAILS: 
            datetime_entitys.extend([RedbackTechDateTimeEntity(coordinator, entity_key)])
    
    async_add_entities(datetime_entitys)
    
class RedbackTechDateTimeEntity(CoordinatorEntity, DateTimeEntity):
    """Representation of Number."""

    def __init__(self, coordinator, entity_key):
        super().__init__(coordinator)
        self.ent_id = entity_key[:7]
        self.ent_key = entity_key
        self.entity_id = 'datetime.rb'+self.ent_id[:4] + '_' + self.ent_id[-3:].lower() + '_' + self.ent_key

    @property
    def ent_data(self) -> ScheduleDateTime:
        """Handle coordinator data for entities."""
        return self.coordinator.data.schedules_datetime_data[self.ent_key]

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
    def native_value(self) -> datetime:
        """Return the state of the entity."""
        LOGGER.debug(self.ent_data.data['value'])
        value = self.ent_data.data['value']
        return value

    async def async_set_value(self, value: datetime) -> None:
        """Update the current value."""
        self.ent_data.data['value'] = value
        LOGGER.debug('datetime_ent_key: %s',self.ent_key)
        LOGGER.debug('datetime_ent_key[-3:]: %s',self.ent_key[-3:])
        LOGGER.debug('datetime_ent_key[4:7]: %s',self.ent_key[4:7])
        
        if self.ent_key[4:7] == 'inv':
            await self.coordinator.client.update_inverter_control_values( self.ent_data.data['device_id'], 'start_time', value)
        elif self.ent_key[4:7] == 'env':
            if self.ent_data.data['entity_name'] == 'op_env_create_start_time':
                await self.coordinator.client.update_op_envelope_values( self.ent_data.data['device_id'], 'StartAtUtc', value)
            elif self.ent_data.data['entity_name'] == 'op_env_create_end_time':
                await self.coordinator.client.update_op_envelope_values( self.ent_data.data['device_id'], 'EndAtUtc', value)

        self.async_write_ha_state()
        #await self.coordinator.async_request_refresh()

