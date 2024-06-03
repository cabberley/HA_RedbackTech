"""DataUpdateCoordinator for the Redback Tech integration."""
#Should be done. Now let's move on to the next file.
from __future__ import annotations

from datetime import timedelta

from redbacktechpy import RedbackTechClient
from redbacktechpy.exceptions import AuthError, RedbackTechClientError
from redbacktechpy.model import RedbackTechData


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_CLIENT_SECRET, CONF_CLIENT_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, POLLING_INTERVAL, TIMEOUT


class RedbackTechDataUpdateCoordinator(DataUpdateCoordinator):
    """RedbackTech Data Update Coordinator."""

    data: RedbackTechData

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the RedbackTech coordinator."""

        try:
            self.client = RedbackTechClient(
                portal_email=entry.data['portal_email'],
                portal_password=entry.data['portal_password'],
                client_id=entry.data[CONF_CLIENT_ID],
                client_secret=entry.data[CONF_CLIENT_SECRET],
                session1=async_get_clientsession(hass),
                session2=async_get_clientsession(hass),
                timeout=TIMEOUT,
            )
            super().__init__(
                hass,
                LOGGER,
                name=DOMAIN,
                update_interval=timedelta(seconds=entry.options[POLLING_INTERVAL]),
            )
        except AuthError as error:
            raise ConfigEntryAuthFailed(error) from error

    async def _async_update_data(self) -> RedbackTechData:
        """Fetch data from Redback Tech."""
        try:
            data = await self.client.get_redback_data()
            LOGGER.debug(f'Found the following Redback devices: {data}')
        except (AuthError) as error:
            raise ConfigEntryAuthFailed(error) from error
        except (RedbackTechClientError) as error:
            raise UpdateFailed(error) from error
        else:
            return data