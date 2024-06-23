"""Sensor platform for Redback Tech integration."""
from __future__ import annotations
from typing import Any

from redbacktechpy.model import Numbers

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberMode,
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
from .number_properties import (
    ENTITY_DETAILS
)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Redback Tech Sensor Entities."""
    global redback_devices, redback_entity_details
    
    coordinator: RedbackTechDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][REDBACKTECH_COORDINATOR]

    redback_devices = coordinator.data.devices    
    redback_entity_details = coordinator.data.entities
    numbers = []

    entity_keys = coordinator.data.numbers.keys()
    for entity_key in entity_keys:
        if entity_key[7:] in  ENTITY_DETAILS: 
            numbers.extend([RedbackTechNumberEntity(coordinator, entity_key)])
    
    async_add_entities(numbers)
    
class RedbackTechNumberEntity(CoordinatorEntity, NumberEntity):
    """Representation of Number."""

    def __init__(self, coordinator, entity_key):
        super().__init__(coordinator)
        self.ent_id = entity_key[:7]
        self.ent_key = entity_key
        self.entity_id = 'number.rb'+self.ent_id[:4] + '_' + self.ent_id[-3:].lower() + '_' + ENTITY_DETAILS[self.ent_key[7:]]['name']
        LOGGER.debug(f'number_data1: {self.ent_data}')
        LOGGER.debug(f'number_data2: {self.ent_id}')

    @property
    def ent_data(self) -> Numbers:
        """Handle coordinator data for entities."""
        return self.coordinator.data.numbers[self.ent_key]

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
        if self.ent_data.data['value'] is None:
            return False    
        return True
    
    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return whether the entity should be enabled by default."""
        if self.ent_data.data['value'] is None:
            return False    
        return True

    @property
    def native_value(self) -> float:
        """Return the state of the entity."""
        LOGGER.debug(self.ent_data.data['value'])
        value = self.ent_data.data['value']
        return value

    @property
    def native_unit_of_measurement(self):
        """Return native Unit of Measurement for this entity."""
        if ENTITY_DETAILS[self.ent_key[7:]]['unit'] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]['unit'] 
        return

    @property
    def device_class(self) -> NumberDeviceClass:
        """Return entity device class."""
        if ENTITY_DETAILS[self.ent_key[7:]]['device_class'] is not None:
            return ENTITY_DETAILS[self.ent_key[7:]]['device_class'] 
        return

    @property
    def mode(self) -> NumberMode:
        """Return box mode."""

        return NumberMode.BOX

    @property
    def native_min_value(self) -> float:
        """Return minimum allowed value."""
        return 0

    @property
    def native_max_value(self) -> float:
        """Return max value allowed."""
        if ENTITY_DETAILS[self.ent_key[7:]]== 'power_setting_watts':
            if redback_entity_details[self.ent_id+'inverter_max_export_power_kw'].data['value'] is not None:
                return redback_entity_details[self.ent_id+'inverter_max_export_power_kw'].data['value']*1000
            else:
                return 15000
        elif ENTITY_DETAILS[self.ent_key[7:]]== 'power_setting_duration':
            return 7200
        return 10000

    @property
    def native_step(self) -> int:
        """Return stepping by 10 grams."""

        return 1

    async def async_set_native_value(self, value: int) -> None:
        """Update the current value."""
        value = int(value)
        self.ent_data.data['value'] = value
        LOGGER.debug('ent_data_value updated: %s',self.ent_data.data['value'])
        if self.ent_key[-3:] == 'inv':
            await self.coordinator.client.update_inverter_control_values( self.ent_data.data['device_id'], self.ent_data.data['entity_name'], value)
        elif self.ent_key[4:7]  == 'env':
            LOGGER.debug('reached env')
            if self.ent_data.data['entity_name'] == 'op_env_create_max_import':
                LOGGER.debug('max_import')
                await self.coordinator.client.update_op_envelope_values( self.ent_data.data['device_id'], 'MaxImportPowerW', value)
            elif self.ent_data.data['entity_name'] == 'op_env_create_max_export':
                LOGGER.debug('max_export')
                await self.coordinator.client.update_op_envelope_values( self.ent_data.data['device_id'], 'MaxExportPowerW', value)
            elif self.ent_data.data['entity_name'] == 'op_env_create_max_discharge':
                await self.coordinator.client.update_op_envelope_values( self.ent_data.data['device_id'], 'MaxDischargePowerW', value)
            elif self.ent_data.data['entity_name'] == 'op_env_create_max_charge':
                await self.coordinator.client.update_op_envelope_values( self.ent_data.data['device_id'], 'MaxChargePowerW', value)
            elif self.ent_data.data['entity_name'] == 'op_env_create_max_generation':
                await self.coordinator.client.update_op_envelope_values( self.ent_data.data['device_id'], 'MaxGenerationPowerVA', value)
                
        self.async_write_ha_state()
