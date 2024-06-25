"""Sensor platform for Redback Tech integration."""

from __future__ import annotations
from typing import Any, Dict
from datetime import datetime
#from redbacktechpy.model import Calendar

from homeassistant.components.calendar import (
    CalendarEvent,
    CalendarEntity,
)
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REDBACKTECH_COORDINATOR, REDBACK_PORTAL, MANUFACTURER, LOGGER
from .coordinator import RedbackTechDataUpdateCoordinator
from .calendar_properties import INVERTER_CALENDAR_DETAILS


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Redback Tech Sensor Entities."""
    global redback_devices, redback_entity_details

    coordinator: RedbackTechDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        REDBACKTECH_COORDINATOR
    ]

    redback_devices = coordinator.data.devices
    #redback_entity_details = coordinator.data.entities
    #calendars = []



    """for device in redback_devices:
        LOGGER.debug("device: %s", device)
        if device[-3:] == "inv" and redback_devices[device].model[:2] != "SI":
            LOGGER.debug("device: %s", device)
            for entity in INVERTER_CALENDAR_DETAILS:
                LOGGER.debug("calendar Entity: %s", entity)
                entity_key = device + entity
                calendars.extend(
                    [RedbackTechCalendarEntity(coordinator, entity_key)]
                )
    """
    redback_entity_details = coordinator.data.inverter_calendar
    calendars = []

    #entity_keys = coordinator.data.numbers.keys()
    for entity in redback_entity_details:
        LOGGER.debug("calendar Entity: %s", entity)
        LOGGER.debug("calendar Entity: %s", entity['device_id'])
        #if entity_key[7:] in ENTITY_DETAILS:
        calendars.extend([RedbackTechCalendarEntity(coordinator, entity)])

    redback_entity_details = coordinator.data.envelope_calendar
    for entity in redback_entity_details:
        #if entity_key[7:] in ENTITY_DETAILS:
        calendars.extend([RedbackTechCalendarEntity(coordinator, entity)])

    async_add_entities(calendars)


class RedbackTechCalendarEntity(CoordinatorEntity, CalendarEntity):
    """Representation of Calendar Entity."""

    def __init__(self, coordinator, entity):
        LOGGER.debug("calendar entity: %s", entity)
        super().__init__(coordinator)
        self.ent_id = entity['device_id']
        #self.ent_key = entity_key
        self.entity_id = (
            "calendar.rb"
            + entity['uuid']
        )
        self._entity = entity
        LOGGER.debug("calendar entity_id: %s",self.entity_id)
        self._event: CalendarEvent | None = None

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
        return self.entity_id

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return False

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._entity['uuid'] #INVERTER_CALENDAR_DETAILS[self.ent_key[7:]]["name"]

    @property
    def extra_state_attributes(self) -> dict:# power_mode(self) -> str:
        """Return the power mode of the entity."""
        res: Dict[str, Any] = {}
        res["uuid"] = self._entity['uuid']
        res["device_id"] = self._entity['device_id']
        return res

    @property
    def event(self) -> CalendarEvent:
        """Return the next upcoming event."""
        if self.coordinator.data and self.coordinator.data.inverter_calendar:
            LOGGER.debug("Found event")
            self._event = CalendarEvent(
                start=self._entity["start"],
                end=self._entity["end"],
                summary=self._entity["summary"],
                description=self._entity["description"],
            )
        else:
            LOGGER.debug("No events found")
            self._event = None
        return self._event

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        return [self._event]

    async def async_delete_event(
        self,
        uid: str,
        recurrence_id: str | None = None,
        recurrence_range: str | None = None,
    ) -> None:
        return

    async def async_create_event(self, **kwargs: Any) -> None:
        return await super().async_create_event(**kwargs)