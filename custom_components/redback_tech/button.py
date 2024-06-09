"""Sensor platform for Redback Tech integration."""
from __future__ import annotations

from math import floor as floor
from typing import Any
from datetime import datetime, timezone 

from homeassistant.components.button import (
    ButtonEntity,
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
from .button_inverter_properties import (
    ENTITY_DETAILS
)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Redback Tech Sensor Entities."""
    global redback_devices
    
    coordinator: RedbackTechDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][REDBACKTECH_COORDINATOR]

    redback_devices = coordinator.data.devices    
    button_entitys = []
    for device in redback_devices:
        LOGGER.debug(f'device: {device}')
        if device[-3:] == 'inv':
            LOGGER.debug(f'device: {device}')
            for entity in ENTITY_DETAILS:
                entity_key = device + entity
                button_entitys.extend([RedbackTechButtonEntity(coordinator, entity_key)])
    
    async_add_entities(button_entitys)
    
    async def handle_reset(call):
        """Handle the service call."""
        device = call.data.get('serial_number')[-4:]+'inv'
        await coordinator.client.delete_all_inverter_schedules(device)
        await coordinator.client.set_inverter_mode_portal(device, True)
        
    async def handle_delete_all_schedules(call):
        device = call.data.get('serial_number')[-4:]+'inv'
        await coordinator.client.delete_all_inverter_schedules(device)

    async def handle_create_schedule(call):
        device = call.data.get('serial_number')[-4:]+'inv'
        mode = call.data.get('mode')
        power = call.data.get('power')
        duration = call.data.get('duration')
        LOGGER.debug(f'device Call data: {call.data}')
        start_time = datetime.strptime(call.data.get('start_time'), "%Y-%m-%d %H:%M:%S").astimezone(timezone.utc)
        LOGGER.debug(f'device Start Time1: {start_time}')
        await coordinator.client.create_schedule_service(device, mode, power, duration, start_time)

    hass.services.async_register(DOMAIN, "inverter_reset_to_auto", handle_reset)
    hass.services.async_register(DOMAIN, "delete_all_schedules", handle_delete_all_schedules)
    hass.services.async_register(DOMAIN, "create_schedule", handle_create_schedule)
    
class RedbackTechButtonEntity(CoordinatorEntity, ButtonEntity):
    """Representation of Number."""

    def __init__(self, coordinator, entity_key):
        super().__init__(coordinator)
        self.ent_id = entity_key[:7]
        self.ent_key = entity_key
        self.entity_id = 'button.rb'+self.ent_id[:4] + '_' + self.ent_id[-3:].lower() + '_' + ENTITY_DETAILS[self.ent_key[7:]]['name']
        LOGGER.debug(f'datetime_data2: {self.ent_id}')

    @property
    def select_data(self):
        """Handle coordinator data for entities."""
        return self.coordinator.data.selects[self.ent_id+'schedule_id_selected'].data['value']

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
        return True
    
    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return whether the entity should be enabled by default."""
        return True

    async def async_press(self) -> None:
        """Update the current value."""
        if self.ent_key[7:] =='create_schedule_event':
            await self.coordinator.client.set_inverter_schedule( redback_devices[self.ent_id].identifiers)
        elif self.ent_key[7:] =='delete_all_schedule_events':
            await self.coordinator.client.delete_all_inverter_schedules( redback_devices[self.ent_id].identifiers)
        elif self.ent_key[7:] =='delete_current_schedule_event':
            await self.coordinator.client.delete_inverter_schedule( redback_devices[self.ent_id].identifiers, self.select_data)
        elif self.ent_key[7:] =='reset_inverter_to_auto':
            await self.coordinator.client.delete_all_inverter_schedules( redback_devices[self.ent_id].identifiers)
            
            await self.coordinator.client.set_inverter_mode_portal(redback_devices[self.ent_id].identifiers, True)
        elif self.ent_key[7:] =='reset_start_time_to_now':
            await self.coordinator.client.reset_inverter_start_time_to_now(redback_devices[self.ent_id].identifiers)
            
        await self.coordinator.async_request_refresh()
    