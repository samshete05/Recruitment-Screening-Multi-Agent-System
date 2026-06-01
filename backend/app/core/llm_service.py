from __future__ import annotations

from typing import Any

import httpx

from app.core.settings import settings


class LLMService:
    def __init__(self) -> None:
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def generate_questions(self, job_title: str, matched_skills: list[str], missing_skills: list[str]) -> list[str]:
        if not self.enabled:
            questions = []
            for skill in matched_skills[:2]:
                questions.append(f"Explain a project where you used {skill} in practice.")
            for skill in missing_skills[:2]:
                questions.append(f"How would you ramp up quickly on {skill} for this role?")
            return questions or ["Walk through your most relevant project for this role."]

        prompt = (
            f"Generate 4 concise interview questions for a {job_title} candidate. "
            f"Matched skills: {', '.join(matched_skills) or 'none'}. "
            f"Missing skills: {', '.join(missing_skills) or 'none'}."
        )
        payload: dict[str, Any] = {
            "model": self.model,
            "input": prompt,
        }
        response = httpx.post(
            "https://api.openai.com/v1/responses",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("output", [{}])[0].get("content", [{}])[0].get("text", "")
        questions = [line.strip("- ").strip() for line in text.splitlines() if line.strip()]
        return questions[:4] or ["Walk through your most relevant project for this role."]
