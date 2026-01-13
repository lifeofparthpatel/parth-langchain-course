SKILLS = {
    "python", "fastapi", "machine learning",
    "nlp", "transformers", "docker",
    "cloud", "pydantic", "async"
}

def extract_skills(text: str) -> set:
    text = text.lower()
    return {s for s in SKILLS if s in text}

def skill_match(job_text, resume_text) -> int:
    job_skills = extract_skills(job_text)
    resume_skills = extract_skills(resume_text)

    if not job_skills:
        return 0

    return round(len(job_skills & resume_skills) / len(job_skills) * 100)
