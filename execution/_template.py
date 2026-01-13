#!/usr/bin/env python3
"""
Template per script di esecuzione.

Questo è un esempio di come strutturare gli script nel livello di esecuzione.
Gli script devono essere:
- Deterministici
- Ben commentati
- Con gestione errori robusta
- Testabili

Uso:
    python execution/_template.py --help
"""

import os
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main(input_path: str, output_path: str) -> bool:
    """
    Funzione principale dello script.
    
    Args:
        input_path: Percorso al file di input
        output_path: Percorso dove salvare l'output
        
    Returns:
        True se l'operazione ha successo, False altrimenti
    """
    try:
        logger.info(f"Elaborazione: {input_path}")
        
        # Verifica che l'input esista
        if not Path(input_path).exists():
            logger.error(f"File non trovato: {input_path}")
            return False
        
        # TODO: Implementa la logica di elaborazione
        
        logger.info(f"Output salvato in: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Errore durante l'elaborazione: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Template script di esecuzione"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Percorso al file di input"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Percorso dove salvare l'output"
    )
    
    args = parser.parse_args()
    
    success = main(args.input, args.output)
    exit(0 if success else 1)
