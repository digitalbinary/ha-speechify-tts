"""Constants for Speechify TTS."""
DOMAIN = "speechify_tts"
CONF_API_KEY = "api_key"
CONF_VOICE_ID = "voice_id"
CONF_MODEL = "model"
CONF_LANGUAGE = "language"

DEFAULT_VOICE_ID = "geffen_32"
DEFAULT_MODEL = "simba-3.5"
DEFAULT_LANGUAGE = "en-US"

STREAM_ENDPOINT = "https://api.speechify.ai/v1/audio/stream"
MODELS = ["simba-3.5", "simba-3.2", "simba-3.0"]

# Cebuano is intentionally included as experimental. Speechify's published
# language table does not list Cebuano as an officially supported locale.
SUPPORTED_LANGUAGES = [
    "en-US", "en-GB", "en-AU", "en-CA", "en-IN",
    "fr-FR", "de-DE", "es-ES", "es-MX", "pt-BR", "pt-PT",
    "it-IT", "ar-AE", "bn-IN", "yue-CN", "da-DK", "nl-NL",
    "et-EE", "fi-FI", "el-GR", "gu-IN", "he-IL", "hi-IN",
    "ja-JP", "ko-KR", "mr-IN", "nb-NO", "pl-PL", "ru-RU",
    "sv-SE", "ta-IN", "te-IN", "tr-TR", "uk-UA", "ur-IN", "vi-VN",
    "ceb-PH",  # experimental; not officially listed by Speechify
]
