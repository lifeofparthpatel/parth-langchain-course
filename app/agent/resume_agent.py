from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from app.agent.tool import calculate_fit
from app.config import OPENAI_API_KEY

def build_resume_agent():
    llm = ChatOpenAI(
        model="gpt-5-mini",
        temperature=0,
        api_key=OPENAI_API_KEY
    )

    return create_agent(
        llm,
        tools=[calculate_fit],
        system_prompt="""
You are ResumeSense.

STRICT RULES:
- NEVER ask the user for input
- You ALWAYS receive job_description and resume_text
- You MUST call the tool `evaluate_candidate`
- You MUST return ONLY the tool result
- NO explanations, NO questions, NO chat
"""
    )
