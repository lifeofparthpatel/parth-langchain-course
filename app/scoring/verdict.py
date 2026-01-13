from app.config import SUITABLE_THRESHOLD, SKILL_MATCH_THRESHOLD

def verdict(score: int) -> str:
    if score >= SUITABLE_THRESHOLD:
        return "Suitable"
    if score >= SKILL_MATCH_THRESHOLD:
        return "Maybe"
    return "Not suitable"
