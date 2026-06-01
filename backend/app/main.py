from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.orchestrator import RecruitmentOrchestrator
from app.models import ScreeningRequest, ScreeningResponse

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Recruitment Screening Multi-Agent System",
    description="A multi-agent recruitment assistant for resume screening and recommendation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
orchestrator = RecruitmentOrchestrator()


@app.get("/")
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/screen", response_model=ScreeningResponse)
def screen_candidates(payload: ScreeningRequest) -> ScreeningResponse:
    return orchestrator.run(payload)
