"""Sensor platform for Redback Tech integration."""

from __future__ import annotations
from typing import Any, Dict
from datetime import datetime

from homeassistant.components.calendar import (
    CalendarEvent,
    CalendarEntity,
    CalendarEntityFeature,
)

from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REDBACKTECH_COORDINATOR, REDBACK_PORTAL, MANUFACTURER, LOGGER
from .coordinator import RedbackTechDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Redback Tech Sensor Entities."""
    if entry.options["include_calendar"]:
        global redback_devices, redback_entity_details

        coordinator: RedbackTechDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
            REDBACKTECH_COORDINATOR
        ]

        redback_devices = coordinator.data.devices

        redback_entity_details = coordinator.data.inverter_calendar
        calendars = []

        for device in redback_devices:
            LOGGER.debug("device: %s", device)
            if device[-3:] == "inv" and redback_devices[device].model[:2] != "SI":
                redback_entity_details = coordinator.data.inverter_calendar
                LOGGER.debug("device: %s", device)
                calendars.extend(
                    [
                        RedbackTechCalendarEntity(
                            coordinator, device, redback_entity_details
                        )
                    ]
                )
            elif device[-3:] == "env":
                redback_entity_details = coordinator.data.envelope_calendar
                LOGGER.debug("device: %s", device)
                calendars.extend(
                    [
                        RedbackTechCalendarEntity(
                            coordinator, device, redback_entity_details
                        )
                    ]
                )
        async_add_entities(calendars)


class RedbackTechCalendarEntity(CoordinatorEntity, CalendarEntity):
    """Representation of Calendar Entity."""

    def __init__(self, coordinator, entity, calendar_details):
        LOGGER.debug("calendar entity: %s", entity)
        super().__init__(coordinator)
        self.ent_id = entity
        # self.ent_key = entity_key
        self.entity_id = "calendar.rb_" + redback_devices[self.ent_id].serial_number
        self.calendar_details = calendar_details
        self._entity = entity
        LOGGER.debug("calendar entity_id: %s", self.entity_id)
        self._event: CalendarEvent | None = None
        self.extra_attributes = {}
        self._attr_supported_features = CalendarEntityFeature.DELETE_EVENT

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        LOGGER.debug("Handle updated data from the coordinator: %s", self._entity)
        if self._entity[-3:] == "inv":
            self.calendar_details = self.coordinator.data.inverter_calendar
        if self._entity[-3:] == "env":
            self.calendar_details = self.coordinator.data.envelope_calendar
        self.async_write_ha_state()

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
        return redback_devices[self.ent_id].serial_number

    @property
    def extra_state_attributes(self) -> dict:
        """Return the power mode of the entity."""
        LOGGER.debug("extra_attributes: %s", self.extra_attributes)
        res: Dict[str, Any] = {}
        if len(self.extra_attributes) > 0:
            res["device_type"] = self.extra_attributes["device_type"]
            res["device_id"] = self.extra_attributes["device_id"]
            res["uuid"] = self.extra_attributes["uuid"]
            res["schedule_selector"] = self.extra_attributes["schedule_selector"]
            if self.extra_attributes["device_type"] == "env":
                res["max_import_power_w"] = self.extra_attributes["max_import_power"]
                res["max_export_power_w"] = self.extra_attributes["max_export_power"]
                res["max_discharge_power_w"] = self.extra_attributes["max_discharge_power"]
                res["max_charge_power_w"] = self.extra_attributes["max_charge_power"]
                res["max_generation_power_va"] = self.extra_attributes[
                    "max_generation_power"
                ]
            elif self.extra_attributes["device_type"] == "inv":
                res["power_level_w"] = self.extra_attributes["power_level"]
                res["power_mode"] = self.extra_attributes["power_mode"]
        return res

    @property
    def event(self) -> CalendarEvent:
        """Return the next upcoming event."""
        if len(self.calendar_details) > 0:
            LOGGER.debug("Found event")
            self.extra_attributes = self.calendar_details[0]
            self._event = CalendarEvent(
                uid=self.calendar_details[0]["uuid"],
                start=self.calendar_details[0]["start"],
                end=self.calendar_details[0]["end"],
                summary=self.calendar_details[0]["summary"],
                description=self.calendar_details[0]["description"],
            )
        else:
            LOGGER.debug("No events found")
            self._event = None
        LOGGER.debug("calendar event: %s", self._event)
        return self._event

    async def async_added_to_hass(self) -> None:
        """Call when entity is added to hass."""
        LOGGER.debug("async_added_to_hass: ")
        await super().async_added_to_hass()
        if self._entity[-3:] == "inv":
            self.calendar_details = self.coordinator.data.inverter_calendar
        if self._entity[-3:] == "env":
            self.calendar_details = self.coordinator.data.envelope_calendar

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        events = []
        for event in self.calendar_details:
            self.extra_attributes = event
            if start_date <= event["start"] <= end_date:
                events.append(
                    CalendarEvent(
                        uid=event["uuid"],
                        start=event["start"],
                        end=event["end"],
                        summary=event["summary"],
                        description=event["description"],
                    )
                )
        LOGGER.debug("calendar events: %s", events)
        return events

    async def async_update(self) -> None:
        """Update the entity."""
        await self.coordinator.async_request_refresh()

    async def async_delete_event(
        self,
        uid: str,
        recurrence_id: str | None = None,
        recurrence_range: str | None = None,
    ) -> None:
        LOGGER.debug("Deleting event: %s", uid)
        for cal_events in self.calendar_details:
            if cal_events["uuid"] == uid:
                if cal_events["device_type"] == "env":
                    schedule_selector = cal_events["uuid"]

                    schedule_selector = schedule_selector.replace(
                        redback_devices[self.ent_id].serial_number + "-", ""
                    )
                    LOGGER.debug("Deleting envelope event: %s", schedule_selector)
                    await self.coordinator.client.delete_op_env_by_id(
                        redback_devices[self.ent_id].identifiers, schedule_selector
                    )
                elif cal_events["device_type"] == "inv":
                    schedule_selector = cal_events["schedule_selector"]
                    await self.coordinator.client.delete_inverter_schedule(
                        redback_devices[self.ent_id].identifiers, schedule_selector
                    )
        await self.coordinator.async_request_refresh()
        return

    async def async_create_event(self, **kwargs: Any) -> None:
        LOGGER.debug("create event: %s", **kwargs)
        return await super().async_create_event(**kwargs)
