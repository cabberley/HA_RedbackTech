"""Redback Tech Component."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN, LOGGER, REDBACKTECH_COORDINATOR, PLATFORMS
from .coordinator import RedbackTechDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up RedbackTech from a config entry."""

    coordinator = RedbackTechDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        REDBACKTECH_COORDINATOR: coordinator
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    LOGGER.info("New Redback Tech integration is setup (entry_id=%s)", entry.entry_id)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""

    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload RedbackTech config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""

    await hass.config_entries.async_reload(entry.entry_id)


async def async_remove_config_entry_device(
    hass: HomeAssistant, entry: ConfigEntry, device_entry: DeviceEntry
) -> bool:
    """Remove RedbackTech config entry."""

    return True


async def async_migrate_entry(hass, entry: ConfigEntry):
    """Migrate outdated Redback config entry."""
    LOGGER.debug("Migrating config entry from version %s", entry.version)

    if entry.version < 3:
        data = {**entry.data}
        version = entry.version + 1
        options = {**entry.options}
        options["include_envelope"] = False
        hass.config_entries.async_update_entry(
            entry, data=data, options=options, version=version
        )
    if entry.version < 4:
        data = {**entry.data}
        version = entry.version + 1
        options = {**entry.options}
        options["portal_inverter_set"] = False
        hass.config_entries.async_update_entry(
            entry, data=data, options=options, version=version
        )
    if entry.version < 5:
        data = {**entry.data}
        version = entry.version + 1
        options = {**entry.options}
        options["include_calendar"] = True
        hass.config_entries.async_update_entry(
            entry, data=data, options=options, version=version
        )
    if entry.version < 6:
        data = {**entry.data}
        version = entry.version + 1
        options = {**entry.options}
        options["include_utility_meters"] = False
        hass.config_entries.async_update_entry(
            entry, data=data, options=options, version=version
        )
    LOGGER.info("Successful migration of config entry to version %s", entry.version)
    return True
