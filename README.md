# Recruitment Screening Multi-Agent System

This project is a recruiter-facing AI screening app built with `FastAPI`, simple `HTML/CSS/JS`, and `Docker`.

It uses six specialized agents to:

- parse resumes
- understand the job description
- match candidate skills
- score and rank candidates
- generate interview questions
- validate recruiter risks

## Project Flow

1. Recruiter enters a job description.
2. Recruiter pastes one or more resumes.
3. FastAPI sends the data into the recruitment orchestrator.
4. Preprocessing cleans the text and extracts skills, experience, and sections.
5. Six agents collaborate to produce final candidate recommendations.
6. The UI shows score, rank, strengths, concerns, and interview questions.

## Agents

1. `Resume Parsing Agent`
2. `Job Understanding Agent`
3. `Matching Agent`
4. `Ranking Agent`
5. `Interview Question Agent`
6. `Validation Agent`




