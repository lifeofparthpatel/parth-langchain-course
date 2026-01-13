from pydantic import BaseModel
from typing import List

class CandidateEvaluation(BaseModel):
    skill_match: int
    experience_years: int
    strengths: List[str]
    gaps: List[str]
    fit_summary: str
    verdict: str
