"""Utilities for RedbackTech Integration"""
#Should be done. Now let's move on to the next file.
from __future__ import annotations

import async_timeout
from aiohttp import ClientError

from redbacktechpy.exceptions import AuthError, RedbackTechClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .client import PortalTolerantRedbackTechClient
from .const import LOGGER, TIMEOUT


async def async_validate_connection(hass: HomeAssistant, client_id: str, client_secret: str, portal_email: str, portal_password: str) -> bool:
    """Get data from API."""

    
    client = PortalTolerantRedbackTechClient(
        portal_email=portal_email,
        portal_password=portal_password,
        client_id=client_id,
        client_secret=client_secret,
        session1=async_get_clientsession(hass),
        session2=async_get_clientsession(hass),
        timeout=TIMEOUT,
    )
    try:
        async with async_timeout.timeout(TIMEOUT):
            test_api = await client.test_api_connection()
    except RedbackTechClientError as err:
        LOGGER.error("Unknown RedbackTech Error: %s", err)
        raise RedbackTechClientError(err) from err
    except AuthError as e:
        LOGGER.debug("Redback API Authentication: %s", e)
        raise AuthError from e

    try:
        async with async_timeout.timeout(TIMEOUT):
            test_portal = await client.test_portal_connection()
    except (AuthError, RedbackTechClientError, ClientError, TimeoutError) as err:
        LOGGER.warning(
            "Redback portal connection failed; API-only setup will continue: %s", err
        )
        await client.async_close_portal_session()
        test_portal = None

    if not test_api:
        LOGGER.error("Could not retrieve any devices from Redback API servers")
        raise NoConnectivityError
    elif test_portal is False:
        LOGGER.warning(
            "Could not retrieve devices from Redback Portal servers; "
            "continuing with API data"
        )
    return True


class NoConnectivityError(Exception):
    """ No Devices from RedbackTech API. """