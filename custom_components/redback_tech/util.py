"""Utilities for RedbackTech Integration"""
#Should be done. Now let's move on to the next file.
from __future__ import annotations

from typing import Any
import async_timeout

from redbacktechpy import RedbackTechClient
from redbacktechpy.exceptions import AuthError, RedbackTechClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import LOGGER, TIMEOUT


async def async_validate_connection(hass: HomeAssistant, client_id: str, client_secret: str, portal_email: str, portal_password: str) -> bool:
    """Get data from API."""

    
    client = RedbackTechClient(
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
        LOGGER.error(f'Unknown RedbackTech Error: {err}')
        raise RedbackTechClientError(err)
    except AuthError as e:
        LOGGER.debug(f"Redback API Authentication: {e}")
        raise AuthError from e

    try:
        async with async_timeout.timeout(TIMEOUT):
            test_portal = await client.test_portal_connection()
    except RedbackTechClientError as err:
        LOGGER.error(f'Unknown RedbackTech Error: {err}')
        raise RedbackTechClientError(err)
    except AuthError as e:
        LOGGER.debug(f"Redback Portal Authentication: {e}")
        raise AuthError from e

    if not test_api:
        LOGGER.error("Could not retrieve any devices from Redback API servers")
        raise NoConnectivityError
    elif not test_portal:
        LOGGER.error("Could not retrieve any devices from Redback Portal servers")
        raise NoConnectivityError
    return True


class NoConnectivityError(Exception):
    """ No Devices from RedbackTech API. """