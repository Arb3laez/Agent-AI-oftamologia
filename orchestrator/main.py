import os
import time
import asyncio
import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from pydantic import BaseModel
from typing import Dict, List, Optional
import structlog
from dotenv import load_dotenv
from prometheus_client import make_asgi_app, Counter, Histogram

load_dotenv()

# Logger
logger = structlog.get_logger()

# App
app = FastAPI(title="Ophthalmology Diagnoses Orchestrator")

# Metrics
DIAGNOSIS_COUNTER = Counter('diagnosis_total', 'Total diagnoses processed')
DIAGNOSIS_LATENCY = Histogram('diagnosis_latency_seconds', 'Time taken for full diagnosis')

# Configuration (URLs of Agent Services)
AGENTS_CONFIG = {
    "GENERAL": os.environ.get("URL_AGENT_GENERAL", "http://agent-general:8000"),
    "RETINA": os.environ.get("URL_AGENT_RETINA", "http://agent-retina:8000"),
    "CORNEA": os.environ.get("URL_AGENT_CORNEA", "http://agent-cornea:8000"),
    "NEURO": os.environ.get("URL_AGENT_NEURO", "http://agent-neuro:8000"),
}
DIRECTOR_URL = os.environ.get("URL_AGENT_DIRECTOR", "http://agent-director:8000")

# Http Client
timeout = httpx.Timeout(120.0, connect=10.0) # Long timeout for LLM
http_client = httpx.AsyncClient(timeout=timeout)

class DiagnosisRequest(BaseModel):
    historial: str

class DiagnosisResponse(BaseModel):
    status: str
    diagnosis: Optional[str] = None
    reports: Optional[Dict[str, str]] = None
    latency_ms: float

@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()

async def call_agent(name: str, url: str, history: str) -> tuple[str, str]:
    """Llama a un agente y retorna (nombre, reporte)."""
    try:
        logger.info("calling_agent", agent=name, url=url)
        response = await http_client.post(f"{url}/analyze", json={"historial": history})
        response.raise_for_status()
        data = response.json()
        return name, data["resultado"]
    except Exception as e:
        logger.error("agent_call_failed", agent=name, error=str(e))
        return name, f"Error al consultar especialista: {str(e)}"

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(request: DiagnosisRequest):
    start_time = time.time()
    
    try:
        # 1. Parallel call to specialists
        logger.info("starting_parallel_diagnosis")
        tasks = []
        for name, url in AGENTS_CONFIG.items():
            tasks.append(call_agent(name, url, request.historial))
            
        results = await asyncio.gather(*tasks)
        
        reports = {name: report for name, report in results}
        
        # 2. Call Director
        logger.info("calling_director")
        director_payload = {
            "historial": request.historial,
            "reportes": reports
        }
        
        director_res = await http_client.post(f"{DIRECTOR_URL}/analyze", json=director_payload)
        director_res.raise_for_status()
        final_diagnosis = director_res.json()["resultado"]
        
        latency = (time.time() - start_time) * 1000
        DIAGNOSIS_COUNTER.inc()
        DIAGNOSIS_LATENCY.observe(latency / 1000)
        
        return DiagnosisResponse(
            status="completed",
            diagnosis=final_diagnosis,
            reports=reports,
            latency_ms=latency
        )
        
    except Exception as e:
        logger.error("orchestration_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Expose Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/health")
def health():
    return {"status": "ok"}
