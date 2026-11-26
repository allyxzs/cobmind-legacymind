from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

Language = Literal["cobol", "fortran", "pli", "unknown"]


class SourceInput(BaseModel):
    filename: str = Field(min_length=1)
    content: str


class CodeNode(BaseModel):
    id: str
    name: str
    kind: str
    line: int | None = None
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)


class Dependency(BaseModel):
    source: str
    target: str
    relation: str
    line: int | None = None


class BusinessRule(BaseModel):
    id: str
    title: str
    description: str
    category: str
    confidence: float = Field(ge=0, le=1)
    line: int | None = None
    evidence: str


class Recommendation(BaseModel):
    priority: Literal["high", "medium", "low"]
    title: str
    rationale: str
    target: str


class AnalysisResult(BaseModel):
    filename: str
    language: Language
    parser: str
    lines: int
    score: int = Field(ge=0, le=100)
    nodes: list[CodeNode]
    dependencies: list[Dependency]
    rules: list[BusinessRule]
    recommendations: list[Recommendation]
    metrics: dict[str, int | float]
    warnings: list[str]
