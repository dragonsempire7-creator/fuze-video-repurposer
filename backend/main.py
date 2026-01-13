from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import logging
from pathlib import Path

app = FastAPI(title="Fuze Agency Video Repurposer API")

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request Models
class TranscribeRequest(BaseModel):
    url: str

class TopicRequest(BaseModel):
    transcript_path: str = ".tmp/transcript.json"

class ResearchRequest(BaseModel):
    topics_path: str = ".tmp/topics.json"

class GenerateRequest(BaseModel):
    transcript_path: str = ".tmp/transcript.json"
    research_path: str = ".tmp/research.json"

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Fuze Agency Backend"}

@app.post("/transcribe")
def transcribe_video(req: TranscribeRequest):
    """
    Step 1: Trascrive Video YouTube usando Apify
    """
    logger.info(f"Ricevuta richiesta trascrizione: {req.url}")
    try:
        cmd = ["python3", "execution/transcribe_video.py", "--url", req.url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Errore script: {result.stderr}")
            raise HTTPException(status_code=500, detail=f"Errore trascrizione: {result.stderr}")
            
        return {"status": "success", "message": "Trascrizione completata", "output": ".tmp/transcript.json"}
    except Exception as e:
        logger.error(f"Eccezione endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
def analyze_topics(req: TopicRequest):
    """
    Step 2: Analizza Topic usando Claude
    """
    try:
        cmd = ["python3", "execution/analyze_topics.py", "--input", req.transcript_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Errore analisi: {result.stderr}")
            
        return {"status": "success", "message": "Analisi completata", "output": ".tmp/topics.json"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research")
def research_topics(req: ResearchRequest):
    """
    Step 3: Ricerca Topic usando Perplexity
    """
    try:
        cmd = ["python3", "execution/research_topics.py", "--input", req.topics_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Errore ricerca: {result.stderr}")
            
        return {"status": "success", "message": "Ricerca completata", "output": ".tmp/research.json"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
def generate_script(req: GenerateRequest):
    """
    Step 4: Genera Script Video usando Claude
    """
    try:
        cmd = [
            "python3", "execution/generate_script.py", 
            "--transcript", req.transcript_path,
            "--research", req.research_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Errore generazione: {result.stderr}")
            
        return {"status": "success", "message": "Script Generato", "output": ".tmp/new_script.md"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
