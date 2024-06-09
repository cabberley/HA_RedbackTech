"""Redback Tech Component."""
#Should be done. Now let's move on to the next file.
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, LOGGER, REDBACKTECH_COORDINATOR, PLATFORMS, UPDATE_LISTENER
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
    
    update_listener = entry.add_update_listener(async_update_options)
    hass.data[DOMAIN][entry.entry_id][UPDATE_LISTENER] = update_listener

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload RedbackTech config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        del hass.data[DOMAIN][entry.entry_id]
        if not hass.data[DOMAIN]:
            del hass.data[DOMAIN]
    return unload_ok

async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """ Update options. """

    await hass.config_entries.async_reload(entry.entry_id)
