from langchain.tools import tool
from app.scoring.skills import extract_skills, skill_match
from app.scoring.verdict import verdict
from app.scoring.experience import extract_years_of_experience

@tool
def calculate_fit(job_description: str, resume_text: str) -> dict:
    """
    Calculate skill match percentage and verdict.
    """

    if not job_description.strip() or not resume_text.strip():
        raise ValueError("Empty input passed to calculate_fit")
    
    job_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    skill_score = skill_match(job_description, resume_text)
    experience_years = extract_years_of_experience(resume_text)

    return {
        "skill_match": skill_score,
        "experience_years": experience_years,
        "matched_skills": list(job_skills & resume_skills),
        "missing_skills": list(job_skills - resume_skills),
        "verdict": verdict(skill_score)
    }
