# Speechify TTS for Home Assistant

Unofficial Home Assistant custom integration that adds a TTS entity backed by Speechify's `POST /v1/audio/stream` API.

> Independent community project; not affiliated with or endorsed by Speechify or Home Assistant.

## Features

- Set up from **Settings → Devices & services → Add integration**.
- Stores the Speechify API key in the Home Assistant config entry.
- Configurable Speechify voice ID, Simba model, and language/locale.
- Requests MP3 audio and returns it to Home Assistant's TTS engine.
- Uses Home Assistant's shared aiohttp session.

## Install from Home Assistant Marketplace

This repository is not yet part of the public Marketplace catalog. Once this repository is published publicly on GitHub:

1. In Home Assistant, open **Settings → Marketplace**.
2. Select **Add from link**.
3. Enter `https://github.com/digitalbinary/ha-speechify-tts` 
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

For the first test, use a known working Speechify voice ID and start with:

- Voice ID: `geffen_32` (the example voice ID supplied for this project)
- Model: `simba-3.5`
- Language: `en-US`

After English works, you can experiment with `ceb-PH`. Cebuano is not listed in Speechify's published language support, so it is not guaranteed to work or sound natural. Filipino (`fil-PH`) has also been listed as coming soon in Speechify's language-support documentation. Check Speechify's current documentation for changes.

- [Speechify streaming API](https://docs.speechify.ai/build/api-reference/v1/audio/stream)
- [Speechify language support](https://docs.speechify.ai/docs/language-support)

## Home Assistant action example

Select the actual Speechify TTS entity created on your system; the entity ID may differ.

```yaml
action: tts.speak
target:
  entity_id: tts.speechify
data:
  media_player_entity_id: media_player.nest_audio
  message: "Maayong gabii, mga suki sa Keylee AI Radio!"
  language: "ceb-PH"
  options:
    voice: "geffen_32"
    model: "simba-3.5"
```

The integration passes the selected voice, model, and language to Speechify. Cebuano is experimental and may be rejected or pronounced poorly by the service.

## Important notes

- The integration buffers the response before returning MP3 bytes to Home Assistant. It does not implement chunk-by-chunk playback.
- This starter implementation has been syntax-checked, but has not been end-to-end tested on a live Home Assistant installation or against a Speechify account.
- Never commit your Speechify API key to this repository. If a key was exposed in a chat, screenshot, repository, or log, revoke it and create a new one.
- Test with short phrases before using it in unattended automations.

## Development

The repository includes GitHub Actions for Home Assistant `hassfest` validation and the HACS/Marketplace action. Check that both workflows pass before publishing a release.
