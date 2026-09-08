"""Redback Tech client customizations."""

from __future__ import annotations

from typing import Any

from aiohttp import ClientError
from redbacktechpy import RedbackTechClient
from redbacktechpy.exceptions import AuthError, RedbackTechClientError

from .const import LOGGER


class PortalTolerantRedbackTechClient(RedbackTechClient):
    """Redback Tech client that treats portal metadata as optional."""

    async def _get_inverter_mppt_data(
        self, serial_numbers: str
    ) -> dict[str, Any]:
        try:
            return await super()._get_inverter_mppt_data(serial_numbers)
        except (
            AuthError,
            RedbackTechClientError,
            ClientError,
            TimeoutError,
        ) as error:
            LOGGER.warning(
                "Redback portal is unavailable; continuing with API data: %s", error
            )
            await self.async_close_portal_session()
            return {}

    async def async_close_portal_session(self) -> None:
        """Close the portal session if the client created one."""
        portal_session = getattr(self, "_session2", None)
        if portal_session is not None and not portal_session.closed:
            await portal_session.close()