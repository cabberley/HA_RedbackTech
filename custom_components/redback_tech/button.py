"""Sensor platform for Redback Tech integration."""
from __future__ import annotations
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
from .button_properties import (
    ENTITY_DETAILS,
    ENTITY_ENVELOPE_DETAILS,
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
        LOGGER.debug('device: %s', device)
        if device[-3:] == 'inv' and redback_devices[device].model[:2] != 'SI':
            LOGGER.debug('device: %s', device)
            for entity in ENTITY_DETAILS:
                entity_key = device + entity
                button_entitys.extend([RedbackTechButtonEntity(coordinator, entity_key)])

        if device[-3:] == 'env':
            LOGGER.debug('device: %s', device)
            for entity in ENTITY_ENVELOPE_DETAILS:
                entity_key = device + entity
                button_entitys.extend([RedbackTechButtonEnvelopeEntity(coordinator, entity_key)])

    async_add_entities(button_entitys)

    async def handle_reset(call):
        """Handle the service call."""
        device = call.data.get('serial_number')[-4:]+'inv'
        await coordinator.client.delete_all_inverter_schedules(device)
        await coordinator.client.set_inverter_mode_portal(device, mode_override=True)
        await coordinator.async_request_refresh()

    async def handle_delete_all_schedules(call):
        device = call.data.get('serial_number')[-4:]+'inv'
        await coordinator.client.delete_all_inverter_schedules(device)
        await coordinator.async_request_refresh()

    async def handle_create_schedule(call):
        device = call.data.get('serial_number')[-4:]+'inv'
        mode = call.data.get('mode')
        power = call.data.get('power')
        duration = call.data.get('duration')
        LOGGER.debug('device Call data: %s',call.data)
        start_time = datetime.strptime(call.data.get('start_time'), "%Y-%m-%d %H:%M:%S").astimezone(timezone.utc)
        LOGGER.debug('device Start Time1: %s',start_time)
        await coordinator.client.create_schedule_service(device, mode, power, duration, start_time)
        await coordinator.async_request_refresh()

    async def handle_set_portal_mode(call):
        device_id = call.data.get('serial_number')[-4:] #+'inv'
        mode = call.data.get('mode1')
        power = call.data.get('power')
        if mode.lower() == 'auto':
            mode = 'Auto'
        elif mode.lower() == 'chargebattery':
            mode = 'ChargeBattery'
        elif mode.lower() == 'dischargebattery':
            mode = 'DischargeBattery'
        elif mode.lower() == 'exportpower':
            mode = 'ExportPower'
        elif mode.lower() == 'importpower':
            mode = 'ImportPower'
        elif mode.lower() == 'conserve':
            mode = 'Conserve'
        LOGGER.debug('device Call set Portal data: %s',call.data)
        await coordinator.client.set_inverter_mode_portal(device_id=device_id, mode=mode, power=power, mode_override=False)
        await coordinator.async_request_refresh()

    async def handle_delete_all_envelopes(call):
        device = call.data.get('site_id')[-4:]+'env'
        await coordinator.client.delete_all_envelopes(device)
        await coordinator.async_request_refresh()
        
    async def handle_delete_single_envelope(call):
        device_id = call.data.get('site_id')[-4:]+'env'
        event_id = call.data.get('event_id')
        await coordinator.client.delete_op_env_by_id(device_id, event_id)
        await coordinator.async_request_refresh()

    async def handle_create_envelope(call):
        event_id = call.data.get('event_id')
        start_at_utc = datetime.strptime(call.data.get('start_time'), "%Y-%m-%d %H:%M:%S").astimezone(timezone.utc)
        end_at_utc = datetime.strptime(call.data.get('end_time'), "%Y-%m-%d %H:%M:%S").astimezone(timezone.utc)
        site_id = call.data.get('site_id')
        max_import_power = call.data.get('max_import_power')
        max_export_power = call.data.get('max_export_power')
        max_discharge_power = call.data.get('max_discharge_power')
        max_charge_power = call.data.get('max_charge_power')
        max_generation_power = call.data.get('max_generation_power')
        await coordinator.client.create_operating_envelope(event_id, start_at_utc, end_at_utc, site_id, max_import_power, max_export_power, max_discharge_power, max_charge_power, max_generation_power)
        await coordinator.async_request_refresh()

    hass.services.async_register(DOMAIN, 'inverter_reset_to_auto', handle_reset)
    hass.services.async_register(DOMAIN, 'delete_all_schedules', handle_delete_all_schedules)
    hass.services.async_register(DOMAIN, 'create_schedule', handle_create_schedule)
    hass.services.async_register(DOMAIN, 'set_portal_mode', handle_set_portal_mode)
    LOGGER.debug('entry.data: %s', entry.data)
    if entry.options['include_envelope']:
        hass.services.async_register(DOMAIN, 'delete_all_envelopes', handle_delete_all_envelopes)
        hass.services.async_register(DOMAIN, 'delete_single_envelope', handle_delete_single_envelope)
        hass.services.async_register(DOMAIN, 'create_operating_envelope', handle_create_envelope)
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
            #self.select_data = None
            await self.coordinator.client.delete_all_inverter_schedules( redback_devices[self.ent_id].identifiers)
        elif self.ent_key[7:] =='delete_current_schedule_event':
            await self.coordinator.client.delete_inverter_schedule( redback_devices[self.ent_id].identifiers, self.select_data)
            #self.select_data = ''
        elif self.ent_key[7:] =='reset_inverter_to_auto':
            #self.select_data = None
            await self.coordinator.client.delete_all_inverter_schedules( redback_devices[self.ent_id].identifiers)
            await self.coordinator.client.set_inverter_mode_portal((redback_devices[self.ent_id].identifiers)[:4], True)
        elif self.ent_key[7:] =='reset_start_time_to_now':
            await self.coordinator.client.reset_inverter_start_time_to_now(redback_devices[self.ent_id].identifiers)
            
        await self.coordinator.async_request_refresh()

class RedbackTechButtonEnvelopeEntity(CoordinatorEntity, ButtonEntity):
    """Representation of Number."""

    def __init__(self, coordinator, entity_key):
        super().__init__(coordinator)
        self.ent_id = entity_key[:7]
        self.ent_key = entity_key
        self.entity_id = 'button.rb'+self.ent_id[:4] + '_' + self.ent_id[-3:].lower() + '_' + ENTITY_ENVELOPE_DETAILS[self.ent_key[7:]]['name']
        LOGGER.debug(f'datetime_data2: {self.ent_id}')

    @property
    def select_data(self):
        """Handle coordinator data for entities."""
        return self.coordinator.data.entities[self.ent_id+'op_env_selected_event_id'].data['value']

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
        return ENTITY_ENVELOPE_DETAILS[self.ent_key[7:]]['name']

    @property
    def icon(self) -> str:
        """Set icon for this entity, if provided in parameters."""
        if ENTITY_ENVELOPE_DETAILS[self.ent_key[7:]]['icon'] is not None:
            return ENTITY_ENVELOPE_DETAILS[self.ent_key[7:]]['icon']
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
        if self.ent_key[7:] =='create_envelope_event':
            LOGGER.debug(f'datetime_data2: {redback_devices[self.ent_id].identifiers}')
            await self.coordinator.client.create_op_envelope( redback_devices[self.ent_id].identifiers)
        elif self.ent_key[7:] =='delete_all_envelope_events':
            #self.select_data = None
            await self.coordinator.client.delete_all_envelopes(redback_devices[self.ent_id].identifiers)
        elif self.ent_key[7:] =='delete_current_envelope_event':
            await self.coordinator.client.delete_op_env_by_id( redback_devices[self.ent_id].identifiers, self.select_data)
            #await self.coordinator.client.delete_op_env_by_id( self.select_data)
            #self.select_data = ''

        await self.coordinator.async_request_refresh()
