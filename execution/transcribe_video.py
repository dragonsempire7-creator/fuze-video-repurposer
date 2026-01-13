#!/usr/bin/env python3
"""
Script per trascrivere video YouTube usando Apify.
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

from apify_client import ApifyClient

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(video_url: str, output_path: str) -> bool:
    try:
        token = os.getenv("APIFY_TOKEN")
        if not token:
            logger.error("APIFY_TOKEN mancante in .env")
            return False

        client = ApifyClient(token)
        
        logger.info(f"Avvio trascrizione per: {video_url}")
        
        # Input per pintostudio/youtube-transcript-scraper
        run_input = {
            "videoUrl": video_url,  # Changed from videoUrls list to single videoUrl string
            "maxItems": 1,
        }

        # Esegui l'Actor
        run = client.actor("pintostudio/youtube-transcript-scraper").call(run_input=run_input)
        
        if not run:
            logger.error("Errore nell'esecuzione dell'Actor Apify")
            return False

        # Recupera i risultati
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
        
        if not dataset_items:
            logger.warning("Nessun dato restituito da Apify")
            return False

        item = dataset_items[0]
        
        # Normalizza output
        # L'output di questo actor varia, adattiamo per ottenere il testo completo
        # Solitamente restituisce una lista di segmenti o un testo full
        
        transcript_text = ""
        segments = []
        
        # Gestione variante output (struttura tipica pintostudio)
        # DEBUG: Dump item keys
        logger.info(f"Item keys: {item.keys()}")
        if "data" in item and isinstance(item["data"], list):
            segments = item["data"]
            transcript_text = " ".join([s.get("text", "").strip() for s in segments])
        elif "text" in item:
             transcript_text = item["text"]
        elif "segments" in item:
            segments = item["segments"]
            transcript_text = " ".join([s.get("text", "") for s in segments])
        
        # Tentativo fallback per struttura diversa
        if not transcript_text and "captions" in item:
             # A volte è sotto 'captions'
             pass
        
        result = {
            "video_url": video_url,
            "title": item.get("title", "Unknown"),
            "channel": item.get("channelName", "Unknown"),
            "transcript": transcript_text,
            "segments": segments
        }

        # Salva output
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Trascrizione salvata in: {output_path}")
        return True

    except Exception as e:
        logger.error(f"Errore trascrizione: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trascrivi video YouTube")
    parser.add_argument("--url", required=True, help="URL del video YouTube")
    parser.add_argument("--output", default=".tmp/transcript.json", help="Path output JSON")
    
    args = parser.parse_args()
    success = main(args.url, args.output)
    exit(0 if success else 1)
