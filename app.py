# app.py - FastAPI Web Server

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from tts_engine import TTSEngine

app = FastAPI(title="Text2Speech")
engine = TTSEngine()

# Mount the output directory so the browser can play/download the audio files
app.mount("/output", StaticFiles(directory="output"), name="output")

class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-AriaNeural"

class BatchRequest(BaseModel):
    text_block: str
    voice: str = "en-US-AriaNeural"

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/voices")
async def api_voices():
    try:
        voices = await engine.get_available_voices(language="en")
        return {"voices": voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/synthesize")
async def api_synthesize(req: TTSRequest):
    try:
        path = await engine.generate_speech(req.text, req.voice)
        return {"success": True, "file": os.path.basename(path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/batch")
async def api_batch(req: BatchRequest):
    try:
        files = await engine.generate_batch(req.text_block, req.voice)
        return {"success": True, "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
