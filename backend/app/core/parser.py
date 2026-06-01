from __future__ import annotations

import re

from app.core.preprocessing import (
    extract_email,
    extract_experience_years,
    extract_name,
    extract_skills,
    normalize_text,
    split_resume_sections,
)


def parse_resume(resume_text: str) -> dict[str, object]:
    normalized = normalize_text(resume_text)
    return {
        "name": extract_name(normalized),
        "email": extract_email(normalized),
        "skills": extract_skills(normalized),
        "experience_years": extract_experience_years(normalized),
        "sections": split_resume_sections(normalized),
        "normalized_text": normalized,
    }


def parse_job_description(job_title: str, job_description: str) -> dict[str, object]:
    normalized = normalize_text(job_description)
    required_skills = extract_skills(normalized)
    experience_match = re.search(r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)", normalized, flags=re.IGNORECASE)
    required_years = float(experience_match.group(1)) if experience_match else 0.0
    return {
        "job_title": job_title,
        "normalized_text": normalized,
        "required_skills": required_skills,
        "required_years": required_years,
    }

