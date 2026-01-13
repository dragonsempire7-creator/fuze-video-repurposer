# Direttiva: Generazione Script Video

## Obiettivo
Creare uno script per un nuovo video YouTube basato sui dati di ricerca e sullo stile del video originale.

## Input
- **Original Transcript**: `.tmp/transcript.json` (per stile/tono).
- **Research Data**: `.tmp/research.json` (contenuto).

## Script di Esecuzione
- `execution/generate_script.py`
  - Usa Claude 3.5 Sonnet.
  - Combina le informazioni per scrivere uno script coinvolgente.

## Output
- File Markdown con lo script completo.
- Path default: `.tmp/new_script.md`

## Prompt
"Agisci come uno YouTuber professionista. Usa le informazioni ricercate per scrivere uno script video coinvolgente. Mantieni un tono simile al transcript originale ma aggiorna i contenuti con le nuove ricerche."
