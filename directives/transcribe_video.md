# Direttiva: Trascrizione Video YouTube

## Obiettivo
Trascrivere un video YouTube dato un URL utilizzando Apify.

## Input
- **Video URL**: URL del video YouTube da trascrivere.

## Script di Esecuzione
- `execution/transcribe_video.py`
  - Usa `apify-client` con l'Actor `pintostudio/youtube-transcript-scraper`.
  - Token API da `.env` (`APIFY_TOKEN`).

## Output
- File JSON contenente il testo trascritto e metadati.
- Path default: `.tmp/transcript.json`

## Struttura Output JSON
```json
{
  "video_url": "...",
  "title": "...",
  "channel": "...",
  "transcript": "Testo completo...",
  "segments": [
    {"text": "...", "start": 0.0, "duration": 2.5},
    ...
  ]
}
```

## Note
- Verifica che l'URL sia valido prima di chiamare Apify.
- Gestisci timeout o errori di Apify.
