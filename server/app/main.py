from __future__ import annotations

import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .audio_analysis import AudioAnalysisError, analyze_media_bytes


MAX_UPLOAD_BYTES = 50 * 1024 * 1024
MAX_UPLOAD_MB = MAX_UPLOAD_BYTES // (1024 * 1024)

app = FastAPI(
    title="VoiceTrace AI API",
    version="0.2.0",
    description="Creator preflight report API for AI voice/video quality checks.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class HealthResult(BaseModel):
    status: str
    version: str
    ffmpeg_available: bool
    max_upload_mb: int


class AnalysisResult(BaseModel):
    filename: str
    content_type: str | None
    size_bytes: int
    analysis_mode: str
    duration_sec: float
    sample_rate: int
    hnr_db: float
    hf_ratio: float
    zero_crossing_rate: float
    clipping_ratio: float
    silence_ratio: float
    upload_readiness: int
    risk_label: str
    series: list[float]
    summary: str
    recommendations: list[str]
    caveat: str


@app.get("/health", response_model=HealthResult)
def health() -> HealthResult:
    return HealthResult(
        status="ok",
        version=app.version,
        ffmpeg_available=shutil.which("ffmpeg") is not None,
        max_upload_mb=MAX_UPLOAD_MB,
    )


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(file: UploadFile = File(...)) -> AnalysisResult:
    content = await file.read()
    size_bytes = len(content)

    if size_bytes == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if size_bytes > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"MVP upload limit is {MAX_UPLOAD_MB}MB.")

    try:
        metrics = analyze_media_bytes(content, file.filename or "upload.bin")
    except AudioAnalysisError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return AnalysisResult(
        filename=file.filename or "unknown",
        content_type=file.content_type,
        size_bytes=size_bytes,
        caveat="HNR/HF ratio and spectral features are quality signals, not proof of AI generation.",
        **metrics,
    )
