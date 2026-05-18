"""Config flow for M3566 RGB Controller."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import M3566ApiClient, M3566ApiError
from .const import DEFAULT_NAME, DEFAULT_PORT, DOMAIN


class M3566RgbConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an M3566 RGB Controller config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            port = user_input[CONF_PORT]
            await self.async_set_unique_id(f"{host}:{port}")
            self._abort_if_unique_id_configured()

            client = M3566ApiClient(
                session=async_get_clientsession(self.hass),
                host=host,
                port=port,
            )
            try:
                await client.async_status()
            except M3566ApiError:
                errors["base"] = "cannot_connect"
            else:
                title = f"{user_input[CONF_NAME]} ({host})"
                return self.async_create_entry(
                    title=title,
                    data={
                        CONF_NAME: user_input[CONF_NAME],
                        CONF_HOST: host,
                        CONF_PORT: port,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
