"""Config Flow for RedbackTech integration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_CLIENT_SECRET, CONF_CLIENT_ID
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from redbacktechpy.exceptions import AuthError, RedbackTechClientError
from .const import DOMAIN, DEFAULT_NAME, POLLING_INTERVAL
from .util import async_validate_connection


DATA_SCHEMA = vol.Schema(
    {
        vol.Required("display_name", default=DEFAULT_NAME): cv.string,
        vol.Required("client_id"): cv.string,
        vol.Required("client_secret"): cv.string,
        vol.Required("portal_email"): cv.string,
        vol.Required("portal_password"): cv.string,
    }
)


class RedbackTechConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Redback Technologies config flow."""

    VERSION = 4
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    entry: config_entries.ConfigEntry | None

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> RedbackTechOptionsFlowHandler:
        """Get the options flow for this handler."""
        return RedbackTechOptionsFlowHandler(config_entry)

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult:
        """Handle re-authentication with redbackTech."""

        self.entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm re-authentication with redbackTech."""

        errors: dict[str, str] = {}

        if user_input:
            client_id = user_input[CONF_CLIENT_ID]
            client_secret = user_input[CONF_CLIENT_SECRET]
            portal_email = user_input["portal_email"]
            portal_password = user_input["portal_password"]

            try:
                await async_validate_connection(
                    self.hass, client_id, client_secret, portal_email, portal_password
                )
            except AuthError:
                errors["base"] = "invalid_auth"
            except RedbackTechClientError:
                errors["base"] = "cannot_connect"
            else:
                assert self.entry is not None

                self.hass.config_entries.async_update_entry(
                    self.entry,
                    data={
                        **self.entry.data,
                        "portal_email": portal_email,
                        "portal_password": portal_password,
                        CONF_CLIENT_ID: client_id,
                        CONF_CLIENT_SECRET: client_secret,
                    },
                    options={
                        POLLING_INTERVAL: self.entry.options[POLLING_INTERVAL],
                        "include_envelope": self.entry.options["include_envelope"],
                        "portal_inverter_set": self.entry.options[
                            "portal_inverter_set"
                        ],
                    },
                )

                await self.hass.config_entries.async_reload(self.entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input:
            client_id = user_input[CONF_CLIENT_ID]
            client_secret = user_input[CONF_CLIENT_SECRET]
            portal_email = user_input["portal_email"]
            portal_password = user_input["portal_password"]

            try:
                await async_validate_connection(
                    self.hass, client_id, client_secret, portal_email, portal_password
                )
            except AuthError:
                errors["base"] = "invalid_auth"
            except RedbackTechClientError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(portal_email)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data={
                        "portal_email": portal_email,
                        "portal_password": portal_password,
                        CONF_CLIENT_ID: client_id,
                        CONF_CLIENT_SECRET: client_secret,
                    },
                    options={
                        POLLING_INTERVAL: 60,
                        "include_envelope": False,
                        "portal_inverter_set": False,
                    },
                )
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reconfiguration of the integration."""
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=DATA_SCHEMA,
        )


class RedbackTechOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle RedbackTech integration options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Required(
                POLLING_INTERVAL,
                default=self.config_entry.options.get(POLLING_INTERVAL, 60),
            ): int,
            vol.Required(
                "include_envelope",
                default=self.config_entry.options.get("include_envelope", False),
            ): cv.boolean,
            vol.Required(
                "portal_inverter_set",
                default=self.config_entry.options.get("portal_inverter_set", False),
            ): cv.boolean,
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))
