# Direttiva: Ricerca Topic (Perplexity)

## Obiettivo
Approfondire i topic estratti effettuando ricerche online mirate usando Perplexity Sonar.

## Input
- **Topics File**: Path al file JSON con i topic (`.tmp/topics.json`).

## Script di Esecuzione
- `execution/research_topics.py`
  - Usa OpenAI Client (OpenRouter) chiamando `perplexity/sonar-medium-online`.
  - Effettua una query per ogni topic identificato.

## Output
- File JSON con i risultati della ricerca.
- Path default: `.tmp/research.json`

## Struttura Output JSON
```json
{
  "research_results": [
    {
      "topic": "Titolo Topic",
      "query": "Query effettuata...",
      "content": "Risultato della ricerca (sintesi/articoli)...",
      "citations": ["url1", "url2"]
    },
    ...
  ]
}
```

## Note
- Perplexity Sonar è ottimizzato per la ricerca online.
- Limita la lunghezza delle risposte per evitare costi eccessivi se ci sono molti topic.
