from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.models import AgentTrace


@dataclass
class BaseAgent:
    agent_id: str
    name: str
    responsibility: str

    def trace(self, summary: str, confidence: float, output: dict[str, Any]) -> AgentTrace:
        return AgentTrace(
            agent_id=self.agent_id,
            agent_name=self.name,
            summary=summary,
            confidence=round(confidence, 2),
            output=output,
        )


class ResumeParsingAgent(BaseAgent):
    def execute(self, context: dict[str, Any]) -> AgentTrace:
        parsed = context["parsed_resume"]
        return self.trace(
            "Parsed the resume into structured candidate information.",
            0.89,
            {
                "candidate_name": parsed["name"],
                "skills_found": parsed["skills"],
                "experience_years": parsed["experience_years"],
            },
        )


class JobUnderstandingAgent(BaseAgent):
    def execute(self, context: dict[str, Any]) -> AgentTrace:
        job = context["parsed_job"]
        return self.trace(
            "Extracted the main role requirements from the job description.",
            0.87,
            {
                "job_title": job["job_title"],
                "required_skills": job["required_skills"],
                "required_years": job["required_years"],
            },
        )


class MatchingAgent(BaseAgent):
    def execute(self, context: dict[str, Any]) -> AgentTrace:
        scorecard = context["scorecard"]
        return self.trace(
            "Matched the candidate profile against the job requirements.",
            0.86,
            {
                "matched_skills": scorecard["matched_skills"],
                "missing_skills": scorecard["missing_skills"],
            },
        )


class RankingAgent(BaseAgent):
    def execute(self, context: dict[str, Any]) -> AgentTrace:
        scorecard = context["scorecard"]
        return self.trace(
            "Calculated a deterministic fit score and recommendation.",
            0.9,
            {
                "score": scorecard["score"],
                "recommendation": scorecard["recommendation"],
            },
        )


class InterviewQuestionAgent(BaseAgent):
    def execute(self, context: dict[str, Any]) -> AgentTrace:
        questions = context["interview_questions"]
        return self.trace(
            "Generated candidate-specific interview questions.",
            0.82,
            {
                "questions": questions,
                "llm_enabled": context["llm_enabled"],
            },
        )


class ValidationAgent(BaseAgent):
    def execute(self, context: dict[str, Any]) -> AgentTrace:
        scorecard = context["scorecard"]
        parsed = context["parsed_resume"]
        concerns = list(scorecard["concerns"])
        if not parsed["email"]:
            concerns.append("Resume does not show a clear email address.")
        if not parsed["skills"]:
            concerns.append("Skill extraction confidence is low because no known skills were found.")
        return self.trace(
            "Reviewed the screening output for confidence gaps and recruiter risks.",
            0.84,
            {
                "concerns": concerns,
                "final_recommendation": scorecard["recommendation"],
            },
        )
