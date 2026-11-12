# Speechify TTS for Home Assistant

Unofficial Home Assistant custom integration that adds a TTS entity backed by Speechify's `POST /v1/audio/stream` API.

> Independent community project; not affiliated with or endorsed by Speechify or Home Assistant.

## Features

- Set up from **Settings → Devices & services → Add integration**.
- Stores the Speechify API key in the Home Assistant config entry.
- Configurable Speechify voice ID, Simba model, language handling, and text normalization.
- Omits the `language` field by default, which is useful for Filipino/Cebuano-English mixed text when you want Speechify to use the selected voice's default locale behavior.
- Sends `options.text_normalization: false` by default to preserve user-provided spelling and pronunciation cues.
- Requests MP3 audio and returns it to Home Assistant's TTS engine.
- Uses Home Assistant's shared aiohttp session.

## Speechify language and normalization settings

The integration now defaults to:

- Model: `simba-3.5`
- Omit language: `true` (the request contains no `language` property)
- Text normalization: `false` (sent as `"options": {"text_normalization": false}`)

This matches the shape of the Speechify API example where the request omits `language` and disables text normalization.

**Important:** Omitting `language` does not guarantee automatic language detection. Speechify may use the selected voice's default locale or apply its own language handling. Test the voice ID with short Filipino and Cebuano samples. If you disable **Omit language parameter**, the locale selected in Home Assistant (or the configured default locale) is sent.

You can change these defaults under **Settings → Devices & services → Speechify TTS → Configure**. The options can also be overridden per `tts.speak` call:

```yaml
action: tts.speak
target:
  entity_id: tts.speechify
data:
  media_player_entity_id: media_player.nest_audio
  message: "Maayong gabii, mga suki sa Kaylee AI Radio! We're back with more great music."
  options:
    voice: "mayumi"
    model: "simba-3.5"
    omit_language: true
    text_normalization: false
```

## Install from Home Assistant Marketplace

This repository is not yet part of the public Marketplace catalog. Once this repository is published publicly on GitHub:

1. In Home Assistant, open **Settings → Marketplace**.
2. Select **Add from link**.
3. Enter `https://github.com/digitalbinary/ha-speechify-tts`.
4. If asked, connect your GitHub account using Home Assistant's device sign-in flow.
5. Add the repository, open its Marketplace page, and select **Install**.
6. Restart Home Assistant if prompted.
7. Go to **Settings → Devices & services → Add integration**, search for **Speechify TTS**, and configure it.

The Marketplace requires a public GitHub repository with a root-level `hacs.json` and the integration under `custom_components/speechify_tts/`.

## Manual install

1. Copy `custom_components/speechify_tts` into your Home Assistant `/config/custom_components/` directory.
2. Restart Home Assistant.
3. Add **Speechify TTS** under **Settings → Devices & services**.

## Initial configuration

Use a Speechify voice ID known to work for your language. For a Filipino test, try the voice ID from your working Speechify sample (for example, `mayumi`) with `simba-3.5`, **Omit language parameter** enabled, and **Text normalization** disabled. Cebuano is not listed as an officially supported Speechify language, so Cebuano pronunciation is experimental and may vary by voice.

- [Speechify streaming API](https://docs.speechify.ai/build/api-reference/v1/audio/stream)
- [Speechify language support](https://docs.speechify.ai/docs/language-support)

## Important notes

- The integration buffers the response before returning MP3 bytes to Home Assistant. It does not implement chunk-by-chunk playback.
- Test with short phrases before using it in unattended automations.
- Never commit your Speechify API key to this repository. If a key was exposed in a chat, screenshot, repository, or log, revoke it and create a new one.

## Development

The repository includes GitHub Actions for Home Assistant `hassfest` validation and the HACS/Marketplace action. Check that both workflows pass before publishing a release.
