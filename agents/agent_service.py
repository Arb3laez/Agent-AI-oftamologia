import os
import sys
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import structlog
from dotenv import load_dotenv

# Add current directory to path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Utils.cliente_groq import ClienteGroq
from Utils.agentes import (
    AgenteOftalmologoGeneral,
    AgenteRetina,
    AgenteCornea,
    AgenteNeuroOftalmologia,
    EquipoMultidisciplinarioOftalmologico
)

load_dotenv()

logger = structlog.get_logger()

app = FastAPI(title="Agente Oftalmológico Service")

# Configuration
AGENT_TYPE = os.environ.get("AGENT_TYPE", "GENERAL").upper() # GENERAL, RETINA, CORNEA, NEURO, DIRECTOR
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.error("startup_failed", reason="GROQ_API_KEY not found")
    # Don't exit here, let k8s restart or fail health check, but better to crash early
    # sys.exit(1)

# Initialize Client
try:
    client = ClienteGroq(api_key=GROQ_API_KEY)
    logger.info("client_initialized")
except Exception as e:
    logger.error("client_init_failed", error=str(e))
    sys.exit(1)

# Initialize Agent based on Type
agent_instance = None

try:
    if AGENT_TYPE == "GENERAL":
        agent_instance = AgenteOftalmologoGeneral(client)
    elif AGENT_TYPE == "RETINA":
        agent_instance = AgenteRetina(client)
    elif AGENT_TYPE == "CORNEA":
        agent_instance = AgenteCornea(client)
    elif AGENT_TYPE == "NEURO":
        agent_instance = AgenteNeuroOftalmologia(client)
    elif AGENT_TYPE == "DIRECTOR":
        agent_instance = EquipoMultidisciplinarioOftalmologico(client)
    else:
        raise ValueError(f"Unknown AGENT_TYPE: {AGENT_TYPE}")
    
    logger.info("agent_initialized", type=AGENT_TYPE, name=getattr(agent_instance, 'nombre', 'Director'))

except Exception as e:
    logger.error("agent_init_failed", error=str(e))
    sys.exit(1)


class AnalysisRequest(BaseModel):
    historial: str
    reportes: dict = {} # Only for Director

class AnalysisResponse(BaseModel):
    resultado: str
    agent: str

@app.get("/health")
def health_check():
    return {"status": "ok", "agent_type": AGENT_TYPE}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    try:
        logger.info("analysis_started", agent=AGENT_TYPE)
        
        if AGENT_TYPE == "DIRECTOR":
            if not request.reportes:
                raise HTTPException(status_code=400, detail="Director requires 'reportes'")
            result = agent_instance.analizar_reportes(request.historial, request.reportes)
        else:
            result = agent_instance.analizar(request.historial)
            
        logger.info("analysis_completed", agent=AGENT_TYPE)
        return AnalysisResponse(resultado=result, agent=AGENT_TYPE)
        
    except Exception as e:
        logger.error("analysis_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
