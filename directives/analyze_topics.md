# Direttiva: Analisi Topic

## Obiettivo
Analizzare una trascrizione video ed estrarre i topic principali usando Claude.

## Input
- **Transcript File**: Path al file JSON generato da `transcribe_video.py`.

## Script di Esecuzione
- `execution/analyze_topics.py`
  - Usa OpenAI Client (configurato per OpenRouter) chiamando `anthropic/claude-3.5-sonnet`.
  - Chiave API da `.env` (`OPENAI_API_KEY`, `OPENAI_BASE_URL`).

## Output
- File JSON con la lista dei topic.
- Path default: `.tmp/topics.json`

## Struttura Output JSON
```json
{
  "topics": [
    "Topic 1: Descrizione...",
    "Topic 2: Descrizione..."
  ],
  "summary": "Breve riassunto del video..."
}
```

## Prompt System
"Sei un assistente esperto in content marketing. Analizza la trascrizione fornita ed estrai 3-5 macro-argomenti principali (topics) che potrebbero essere spunti per nuovi contenuti video. Fornisci un breve riassunto per ognuno."
