from __future__ import annotations

import re


KNOWN_SKILLS = {
    "python",
    "fastapi",
    "flask",
    "django",
    "sql",
    "mysql",
    "postgresql",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "java",
    "javascript",
    "typescript",
    "react",
    "node.js",
    "node",
    "machine learning",
    "deep learning",
    "pandas",
    "numpy",
    "power bi",
    "excel",
    "git",
    "rest api",
    "microservices",
}


def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z0-9.+#-]+", text.lower()) if len(token) > 1}


def extract_email(text: str) -> str | None:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None


def extract_name(text: str) -> str:
    first_line = normalize_text(text).split("\n", maxsplit=1)[0]
    first_line = re.sub(r"[^A-Za-z ]", "", first_line).strip()
    return first_line or "Unknown Candidate"


def extract_experience_years(text: str) -> float:
    lowered = text.lower()
    matches = re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)", lowered)
    if matches:
        return max(float(item) for item in matches)
    return 0.0


def extract_skills(text: str) -> list[str]:
    lowered = text.lower()
    found = [skill for skill in KNOWN_SKILLS if skill in lowered]
    return sorted(found)


def split_resume_sections(text: str) -> dict[str, str]:
    normalized = normalize_text(text)
    patterns = {
        "skills": r"(skills|technical skills)",
        "experience": r"(experience|work experience|professional experience)",
        "education": r"(education|academic background)",
        "projects": r"(projects|project experience)",
    }
    sections: dict[str, str] = {}
    for name, pattern in patterns.items():
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if match:
            start = match.start()
            sections[name] = normalized[start : start + 800]
    return sections

