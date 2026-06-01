from __future__ import annotations

from app.core.agents import (
    InterviewQuestionAgent,
    JobUnderstandingAgent,
    MatchingAgent,
    RankingAgent,
    ResumeParsingAgent,
    ValidationAgent,
)
from app.core.llm_service import LLMService
from app.core.parser import parse_job_description, parse_resume
from app.core.scoring import score_candidate
from app.models import CandidateResult, ScreeningRequest, ScreeningResponse


class RecruitmentOrchestrator:
    def __init__(self) -> None:
        self.llm = LLMService()
        self.agents = [
            ResumeParsingAgent("resume-parser", "Resume Parsing Agent", "Extracts structure from resume text."),
            JobUnderstandingAgent("job-understanding", "Job Understanding Agent", "Extracts the role requirements."),
            MatchingAgent("matching-agent", "Matching Agent", "Compares resume and job requirements."),
            RankingAgent("ranking-agent", "Ranking Agent", "Scores and ranks candidates."),
            InterviewQuestionAgent("question-agent", "Interview Question Agent", "Creates tailored interview questions."),
            ValidationAgent("validation-agent", "Validation Agent", "Flags confidence gaps and mismatch risks."),
        ]

    def run(self, payload: ScreeningRequest) -> ScreeningResponse:
        parsed_job = parse_job_description(payload.job_title, payload.job_description)
        results: list[CandidateResult] = []

        for resume in payload.resumes:
            parsed_resume = parse_resume(resume.resume_text)
            scorecard = score_candidate(parsed_resume, parsed_job)
            interview_questions = self.llm.generate_questions(
                payload.job_title,
                scorecard["matched_skills"],
                scorecard["missing_skills"],
            )

            context = {
                "parsed_resume": parsed_resume,
                "parsed_job": parsed_job,
                "scorecard": scorecard,
                "interview_questions": interview_questions,
                "llm_enabled": self.llm.enabled,
            }
            traces = [agent.execute(context) for agent in self.agents]

            results.append(
                CandidateResult(
                    candidate_id=resume.candidate_id,
                    candidate_name=str(parsed_resume["name"]),
                    score=float(scorecard["score"]),
                    rank=0,
                    recommendation=scorecard["recommendation"],
                    matched_skills=scorecard["matched_skills"],
                    missing_skills=scorecard["missing_skills"],
                    strengths=scorecard["strengths"],
                    concerns=traces[-1].output["concerns"],
                    interview_questions=interview_questions,
                    traces=traces,
                )
            )

        results.sort(key=lambda item: item.score, reverse=True)
        for index, item in enumerate(results, start=1):
            item.rank = index

        shortlist_count = sum(1 for item in results if item.recommendation == "shortlist")
        summary = (
            f"Screened {len(results)} candidates for {payload.job_title}. "
            f"{shortlist_count} candidates reached shortlist status."
        )
        return ScreeningResponse(
            job_title=payload.job_title,
            total_candidates=len(results),
            screening_summary=summary,
            results=results,
        )
