from __future__ import annotations


def score_candidate(candidate: dict[str, object], job: dict[str, object]) -> dict[str, object]:
    candidate_skills = set(candidate["skills"])
    required_skills = set(job["required_skills"])
    matched_skills = sorted(candidate_skills & required_skills)
    missing_skills = sorted(required_skills - candidate_skills)

    skill_score = (len(matched_skills) / max(len(required_skills), 1)) * 70
    experience_gap = max(float(job["required_years"]) - float(candidate["experience_years"]), 0.0)
    experience_score = 30 if experience_gap <= 0 else max(10, 30 - (experience_gap * 10))
    final_score = round(skill_score + experience_score, 2)

    if final_score >= 75:
        recommendation = "shortlist"
    elif final_score >= 50:
        recommendation = "review"
    else:
        recommendation = "reject"

    strengths = []
    concerns = []

    if matched_skills:
        strengths.append(f"Matched skills: {', '.join(matched_skills[:5])}")
    if float(candidate["experience_years"]) >= float(job["required_years"]):
        strengths.append("Experience level meets or exceeds the job requirement.")
    if missing_skills:
        concerns.append(f"Missing skills: {', '.join(missing_skills[:5])}")
    if experience_gap > 0:
        concerns.append(f"Experience gap of about {experience_gap:.1f} years against the role expectation.")

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score": final_score,
        "recommendation": recommendation,
        "strengths": strengths or ["General alignment with the role was detected."],
        "concerns": concerns or ["No major risk signals from deterministic screening."],
    }

