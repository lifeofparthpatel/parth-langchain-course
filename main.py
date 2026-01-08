import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langsmith import Client
from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse, JobPosting
from langchain_core.tools.render import render_text_description
from langchain_classic.agents.output_parsers import ReActSingleInputOutputParser  

# =========================
# Environment Setup
# =========================
load_dotenv()

# =========================
# Tool Definitions
# =========================
@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )  # stripping away non alphabetic characters just in case

    return len(text)


# =========================
# Main Entry Point
# =========================
def main():
    print("Starting the job posting agent...")
    tools = [get_text_length]
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools= render_text_description(tools),
        tool_names=", ".join([tool.name for tool in tools]),
    )

    llm = ChatOpenAI(model="gpt-4", temperature=0, model_kwargs={"stop": ["\nObervation", "Observation", "Observation:"]})
    agent = {"input": lambda x:x["input"]} | prompt | llm | ReActSingleInputOutputParser()
    response = agent.invoke({"input": "What is the length of the following: 'Hello, world!'"})
    print("Agent response:", response)
# =========================
# Script Execution Guard
# =========================
if __name__ == "__main__":
    main()