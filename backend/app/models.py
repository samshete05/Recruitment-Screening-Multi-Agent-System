from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ResumeInput(BaseModel):
    candidate_id: str = Field(..., min_length=1, max_length=40)
    resume_text: str = Field(..., min_length=40, max_length=12000)


class ScreeningRequest(BaseModel):
    job_title: str = Field(..., min_length=2, max_length=120)
    job_description: str = Field(..., min_length=60, max_length=12000)
    resumes: list[ResumeInput] = Field(..., min_length=1, max_length=20)


class AgentTrace(BaseModel):
    agent_id: str
    agent_name: str
    summary: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    output: dict[str, Any]


class CandidateResult(BaseModel):
    candidate_id: str
    candidate_name: str
    score: float
    rank: int
    recommendation: Literal["shortlist", "review", "reject"]
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    concerns: list[str]
    interview_questions: list[str]
    traces: list[AgentTrace]


class ScreeningResponse(BaseModel):
    job_title: str
    total_candidates: int
    screening_summary: str
    results: list[CandidateResult]

