#!/usr/bin/env python3
"""
Script per analizzare topic da trascrizione usando Claude (via OpenRouter).
"""

import os
import json
import argparse
import logging
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from openai import OpenAI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(input_path: str, output_path: str) -> bool:
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key or not base_url:
            logger.error("Credenziali OpenRouter mancanti in .env")
            return False
            
        if not Path(input_path).exists():
            logger.error(f"File input non trovato: {input_path}")
            return False
            
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            transcript = data.get("transcript", "")
            
        if not transcript:
            logger.error("Trascrizione vuota o mancante")
            return False
            
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        logger.info("Invio richiesta a Claude...")
        
        prompt = f"""
        Analizza la seguente trascrizione di un video YouTube ed estrai i 5 argomenti (topics) principali.
        Per ogni topic, fornisci un titolo e una breve descrizione.
        
        Restituisci ESCLUSIVAMENTE un JSON valido con questa struttura:
        {{
            "summary": "Breve riassunto generale del video",
            "topics": [
                {{"title": "Topic 1", "description": "Dettagli..."}},
                ...
            ]
        }}
        
        TRASCRIZIONE:
        {transcript[:15000]}  # Tronca se troppo lungo per contesto (placeholder)
        """
        
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=[
                {"role": "system", "content": "Sei un content strategist AI. Rispondi solo in JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Analisi salvata in: {output_path}")
        return True

    except Exception as e:
        logger.error(f"Errore analisi topic: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=".tmp/transcript.json", help="Path trascrizione JSON")
    parser.add_argument("--output", default=".tmp/topics.json", help="Path output JSON")
    
    args = parser.parse_args()
    success = main(args.input, args.output)
    exit(0 if success else 1)
