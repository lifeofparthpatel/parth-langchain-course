import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SKILL_MATCH_THRESHOLD = 50
SUITABLE_THRESHOLD = 70
