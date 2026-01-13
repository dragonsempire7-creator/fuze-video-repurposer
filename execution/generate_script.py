#!/usr/bin/env python3
"""
Script per generare il nuovo video script usando Claude.
"""

import os
import json
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(transcript_path: str, research_path: str, output_path: str) -> bool:
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key: return False

        # Load inputs
        if not Path(transcript_path).exists() or not Path(research_path).exists():
            logger.error("File di input mancanti")
            return False

        with open(transcript_path, "r", encoding="utf-8") as f:
            trans_data = json.load(f)
            original_text = trans_data.get("transcript", "")[:5000] # Context limit

        with open(research_path, "r", encoding="utf-8") as f:
            res_data = json.load(f)
            research_text = json.dumps(res_data.get("research_results", []), indent=2, ensure_ascii=False)

        client = OpenAI(api_key=api_key, base_url=base_url)
        
        prompt = f"""
        Scrivi uno script completo per un video YouTube.
        
        ISTRUZIONI CRITICHE:
        1. **STILE E TONO**: Devi ASSOLUTAMENTE imitare lo stile, il ritmo e la personalità trovati nel "TRANSCRIPT ORIGINALE".
        2. **CONTENUTO**: Devi arricchire e aggiornare i contenuti usando i fatti trovati nelle "FONTI RICERCA".
        
        TRANSCRIPT ORIGINALE (Usa SOLO per Stile/Tono):
        {original_text}
        
        FONTI RICERCA (Usa per Contenuto/Fatti Nuovi):
        {research_text}
        
        STRUTTURA DESIDERATA PER IL NUOVO VIDEO:
        1. Hook (Primi 30s: cattura attenzione usando lo stile dello speaker originale)
        2. Intro Sigla (breve)
        3. Body Point 1, 2, 3... (Contenti aggiornati dalle ricerche, esposti con la voce dello speaker)
        4. Conclusion & CTA
        
        Output in formato Markdown ben formattato.
        """
        
        logger.info("Generazione script in corso...")
        
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=[
                {"role": "system", "content": "Sei un esperto copywriter per YouTube."},
                {"role": "user", "content": prompt}
            ]
        )
        
        script_content = response.choices[0].message.content
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_content)
            
        logger.info(f"Script generato in: {output_path}")
        return True

    except Exception as e:
        logger.error(f"Errore generazione: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", default=".tmp/transcript.json")
    parser.add_argument("--research", default=".tmp/research.json")
    parser.add_argument("--output", default=".tmp/new_script.md")
    
    args = parser.parse_args()
    success = main(args.transcript, args.research, args.output)
    exit(0 if success else 1)
