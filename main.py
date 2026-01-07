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

# =========================
# Environment Setup
# =========================
load_dotenv()

# =========================
# (Optional) Tavily Client
# =========================
# tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

# =========================
# (Optional) Custom Tool
# =========================
# @tool(description="Search for job information of a given city")
# def search_tool(query: str) -> str:
#     print(f'Searching for: {query}')
#     return tavily.search(query=query)


# =========================
# LLM Configuration
# =========================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# =========================
# Tools Configuration
# =========================
# tools = [search_tool]
tools = [TavilySearch()]

# =========================
# Output Parser (Structured Output)
# =========================
output_parser = PydanticOutputParser(
    pydantic_object=AgentResponse
)

# =========================
# ReAct Prompt with Format Instructions
# =========================
react_prompt_with_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=[
        "input",
        "tools",
        "tool_names",
        "format_instructions",
        "agent_scratchpad"
    ],
).partial(
    format_instructions=output_parser.get_format_instructions()
)

# =========================
# Agent Creation (ReAct)
# =========================
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_instructions
)

# =========================
# Agent Executor
# =========================
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

extract_output = RunnableLambda(
    lambda x: x["output"]
)
parse_output = RunnableLambda(lambda x: output_parser.parse(x))
# Alias for clarity
chain = agent_executor | extract_output | parse_output

# =========================
# (Alternative Modern Agent — NOT USED)
# =========================
# agent = create_agent(
#     model=llm,
#     tools=tools,
#     response_format=AgentResponse
# )


# =========================
# Main Entry Point
# =========================
def main():
    print("Hello from parth-langchain-course!")

    # Example direct agent invocation (commented)
    # result = agent.invoke(
    #     {
    #         "messages": HumanMessage(
    #             content=(
    #                 "Search for 3 job posting for AI engineer using LangChain "
    #                 "in Ahmedabad, Gujarat, India on Naukri and list their details."
    #             )
    #         )
    #     }
    # )

    # ReAct Agent Execution
    result = chain.invoke(
        input={
            "input": (
                "Search for 3 job posting for AI engineer using LangChain "
                "in Ahmedabad, Gujarat, India on Naukri and list their details."
            )
        }
    )

    print("Agent Result:", result)


# =========================
# Script Execution Guard
# =========================
if __name__ == "__main__":
    main()