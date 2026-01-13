# App-Antigravity

Ambiente di sviluppo strutturato con architettura a 3 livelli per massimizzare l'affidabilità.

## Struttura

```
├── directives/     # SOP in Markdown (Livello 1: Cosa fare)
├── execution/      # Script Python deterministici (Livello 3: Esecuzione)
├── .tmp/           # File intermedi (mai committare)
├── .env            # Variabili d'ambiente e chiavi API
└── GEMINI.md       # Istruzioni per l'agente AI
```

## Come Funziona

1. **Direttive** (`directives/`): Istruzioni scritte che definiscono obiettivi, input, output e casi limite
2. **Orchestrazione**: L'agente AI legge le direttive e decide quali script eseguire
3. **Esecuzione** (`execution/`): Script Python che fanno il lavoro effettivo in modo deterministico

## Setup

1. Copia `.env.example` in `.env`
2. Compila le chiavi API necessarie
3. Installa le dipendenze Python: `pip install -r requirements.txt` (quando creato)

## Regole

- I file in `.tmp/` sono sempre rigenerabili
- I deliverable vivono su servizi cloud (Google Sheets, ecc.)
- Aggiorna le direttive quando impari qualcosa di nuovo
