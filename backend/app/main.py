from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .analyzer import analyze
from .models import AnalysisResult, SourceInput

SAMPLES_DIR = Path(__file__).resolve().parents[2] / "samples"
SAMPLE_FILES = {
    "custmstr": "CUSTMSTR.cbl",
    "interest": "INTEREST.cbl",
    "payroll": "payroll.f90",
    "acctrec": "acctrec.pli",
}

app = FastAPI(title="CobMind LegacyMind API", version="0.1.0", description="Análise estática de sistemas legados.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "cobmind-api", "version": app.version}

@app.post("/api/v1/analyze", response_model=AnalysisResult)
def analyze_source(source: SourceInput):
    if len(source.content) > 2_000_000:
        raise HTTPException(status_code=413, detail="Arquivo excede o limite de 2 MB")
    return analyze(source.filename, source.content)

@app.post("/api/v1/analyze/file", response_model=AnalysisResult)
async def analyze_file(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8", errors="replace")
    if len(content) > 2_000_000:
        raise HTTPException(status_code=413, detail="Arquivo excede o limite de 2 MB")
    return analyze(file.filename or "uploaded-source", content)

@app.get("/api/v1/languages")
def languages():
    return {"languages": [{"id": "cobol", "extensions": [".cbl", ".cob"]}, {"id": "fortran", "extensions": [".f", ".f90"]}, {"id": "pli", "extensions": [".pli", ".pl1"]}]}

@app.get("/api/v1/samples/{sample_id}")
def get_sample(sample_id: str):
    filename = SAMPLE_FILES.get(sample_id)
    if not filename:
        raise HTTPException(status_code=404, detail="Amostra não encontrada")
    path = SAMPLES_DIR / filename
    if not path.is_file():
        raise HTTPException(status_code=500, detail="Arquivo de amostra ausente no volume samples/")
    return {"filename": filename, "content": path.read_text(encoding="utf-8", errors="replace")}
