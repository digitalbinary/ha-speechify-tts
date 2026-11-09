"""Config flow for Speechify TTS."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import OptionsFlowWithReload
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_API_KEY,
    CONF_LANGUAGE,
    CONF_MODEL,
    CONF_VOICE_ID,
    DEFAULT_LANGUAGE,
    DEFAULT_MODEL,
    DEFAULT_VOICE_ID,
    DOMAIN,
    MODELS,
)


class SpeechifyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Speechify setup."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Set up the integration.

        We do not call a guessed validation endpoint during setup. The API key
        is verified naturally when the first TTS request is made.
        """
        if user_input is not None:
            await self.async_set_unique_id("speechify_tts")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Speechify TTS", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Optional(CONF_VOICE_ID, default=DEFAULT_VOICE_ID): str,
                vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): vol.In(MODELS),
                vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Return the options flow."""
        return SpeechifyOptionsFlow()


class SpeechifyOptionsFlow(OptionsFlowWithReload):
    """Allow changing voice, model and language after setup."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_VOICE_ID,
                    default=current.get(CONF_VOICE_ID, DEFAULT_VOICE_ID),
                ): str,
                vol.Required(
                    CONF_MODEL,
                    default=current.get(CONF_MODEL, DEFAULT_MODEL),
                ): vol.In(MODELS),
                vol.Required(
                    CONF_LANGUAGE,
                    default=current.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
                ): str,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
