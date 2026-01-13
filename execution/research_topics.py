#!/usr/bin/env python3
"""
Script per ricercare topics usando Perplexity Sonar (via OpenRouter).
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
        
        if not api_key:
            logger.error("API Key mancante")
            return False

        if not Path(input_path).exists():
            logger.error(f"File topics non trovato: {input_path}")
            return False

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            topics = data.get("topics", [])

        if not topics:
            logger.warning("Nessun topic trovato da ricercare")
            return False

        client = OpenAI(api_key=api_key, base_url=base_url)
        results = []

        logger.info(f"Avvio ricerca per {len(topics)} topics...")

        for topic in topics:
            title = topic.get("title", "Unknown Topic")
            description = topic.get("description", "")
            
            query_prompt = f"Cerca informazioni recenti e approfondite su: {title}. Contesto: {description}"
            logger.info(f"Ricerca: {title}")

            response = client.chat.completions.create(
                model="perplexity/sonar",
                messages=[
                    {"role": "system", "content": "Sei un motore di ricerca esperto. Fornisci risposte dettagliate e citali fonti."},
                    {"role": "user", "content": query_prompt}
                ]
            )
            
            content = response.choices[0].message.content
            # OpenRouter/Perplexity a volte mettono le citazioni in campi specifici o nel testo
            # Per semplicità salviamo il contenuto testuale
            
            results.append({
                "topic": title,
                "query": query_prompt,
                "content": content
            })

        output_data = {"research_results": results}
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Ricerca completata, salvata in: {output_path}")
        return True

    except Exception as e:
        logger.error(f"Errore ricerca: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=".tmp/topics.json", help="Path topics JSON")
    parser.add_argument("--output", default=".tmp/research.json", help="Path output JSON")
    
    args = parser.parse_args()
    success = main(args.input, args.output)
    exit(0 if success else 1)
