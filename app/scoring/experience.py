import re

def extract_years_of_experience(text: str) -> int:
    """
    Very conservative heuristic:
    looks for patterns like '3 years', '5+ years'
    """
    matches = re.findall(r'(\d+)\+?\s+years?', text.lower())
    years = [int(m) for m in matches]
    return max(years) if years else 0


def experience_match(resume_text: str, required_years: int) -> bool:
    return extract_years_of_experience(resume_text) >= required_years
