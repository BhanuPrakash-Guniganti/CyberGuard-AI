from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.app.core.config import settings
from backend.app.core.database import db_manager
from backend.app.api.auth import router as auth_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.events import router as events_router
from backend.app.api.alerts import router as alerts_router
from backend.app.api.incidents import router as incidents_router
from backend.app.api.investigation import router as investigation_router
from backend.app.api.rag import router as rag_router
from backend.app.api.response import router as response_router
from backend.app.api.audit import router as audit_router
from backend.app.api.reports import router as reports_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cyberguard.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("[*] Starting CyberGuard AI Backend Service...")
    await db_manager.connect()
    yield
    logger.info("[*] Shutting down CyberGuard AI Backend Service...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Generative AI Framework for Cyber Threat Detection, Automated Incident Investigation and Defensive Response Simulation",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev/demo simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(events_router, prefix=settings.API_V1_STR)
app.include_router(alerts_router, prefix=settings.API_V1_STR)
app.include_router(incidents_router, prefix=settings.API_V1_STR)
app.include_router(investigation_router, prefix=settings.API_V1_STR)
app.include_router(rag_router, prefix=settings.API_V1_STR)
app.include_router(response_router, prefix=settings.API_V1_STR)
app.include_router(audit_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "framework": "CyberGuard AI",
        "version": settings.VERSION,
        "status": "ONLINE",
        "simulation_mode": True,
        "disclaimer": "Simulation Only — Actual Infrastructure Not Modified."
    }

@app.get("/health")
async def health_check():
    return {
        "status": "HEALTHY",
        "ml_engine": "ACTIVE",
        "rag_retriever": "ACTIVE",
        "database": "CONNECTED"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
