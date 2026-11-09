"""Speechify text-to-speech entity."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
from homeassistant.components.tts import TextToSpeechEntity, TtsAudioType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    CONF_API_KEY,
    CONF_LANGUAGE,
    CONF_MODEL,
    CONF_VOICE_ID,
    DEFAULT_LANGUAGE,
    DEFAULT_MODEL,
    DEFAULT_VOICE_ID,
    DOMAIN,
    STREAM_ENDPOINT,
    SUPPORTED_LANGUAGES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Speechify TTS entity."""
    async_add_entities([SpeechifyTTSEntity(hass, entry)])


class SpeechifyTTSEntity(TextToSpeechEntity):
    """Generate MP3 audio using Speechify's streaming API endpoint."""

    _attr_has_entity_name = True
    _attr_name = "Speechify"
    _attr_supported_languages = SUPPORTED_LANGUAGES
    _attr_supported_options = ["voice", "model"]

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self.hass = hass
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_tts"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Speechify TTS",
            manufacturer="Speechify",
            model="Speechify AI TTS API",
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def _settings(self) -> dict[str, Any]:
        """Return config data with options taking precedence."""
        return {**self.entry.data, **self.entry.options}

    @property
    def default_language(self) -> str:
        """Return configured default language."""
        return self._settings.get(CONF_LANGUAGE, DEFAULT_LANGUAGE)

    @property
    def default_options(self) -> dict[str, Any]:
        """Return configured voice and model."""
        settings = self._settings
        return {
            "voice": settings.get(CONF_VOICE_ID, DEFAULT_VOICE_ID),
            "model": settings.get(CONF_MODEL, DEFAULT_MODEL),
        }

    async def async_get_tts_audio(
        self, message: str, language: str, options: dict[str, Any]
    ) -> TtsAudioType:
        """Request an MP3 from Speechify and return it to Home Assistant."""
        if not message.strip():
            raise HomeAssistantError("Speechify received an empty message.")
        if len(message) > 32000:
            raise HomeAssistantError("Speechify input exceeds 32,000 characters.")

        settings = self._settings
        payload = {
            "input": message,
            "voice_id": options.get(
                "voice", settings.get(CONF_VOICE_ID, DEFAULT_VOICE_ID)
            ),
            "model": options.get(
                "model", settings.get(CONF_MODEL, DEFAULT_MODEL)
            ),
            "language": language or settings.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
        }

        session = async_get_clientsession(self.hass)
        try:
            async with session.post(
                STREAM_ENDPOINT,
                json=payload,
                headers={
                    "Authorization": f"Bearer {settings[CONF_API_KEY]}",
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg",
                },
                timeout=aiohttp.ClientTimeout(total=180),
            ) as response:
                if response.status >= 400:
                    detail = (await response.text())[:500]
                    _LOGGER.error(
                        "Speechify API returned HTTP %s: %s", response.status, detail
                    )
                    raise HomeAssistantError(
                        f"Speechify API error {response.status}: {detail}"
                    )
                audio = await response.read()
                if not audio:
                    raise HomeAssistantError("Speechify returned empty audio.")
                content_type = response.headers.get("Content-Type", "")
                if "json" in content_type.lower():
                    raise HomeAssistantError(
                        "Speechify returned JSON instead of audio; expected audio/mpeg."
                    )
                return "mp3", audio
        except aiohttp.ClientError as err:
            raise HomeAssistantError(f"Could not connect to Speechify: {err}") from err
        except TimeoutError as err:
            raise HomeAssistantError("Speechify request timed out.") from err
