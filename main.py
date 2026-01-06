from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import os
load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
# from tavily import TavilyClient

# tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

# @tool(description="Search for job information of a given city")
# def search_tool(query: str) -> str:
#     print(f'Searching for: {query}')
#     return tavily.search(query=query)

llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
# tools = [search_tool]
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)

def main():
    print("Hello from parth-langchain-course!")
    result = agent.invoke(
        {
    "messages": HumanMessage(content="Search for 3 job posting for ai engineer using langchain in ahmedabad, gujarat, india on Naukri and list their details.")
}
)

    print('Agent Result:', result)

if __name__ == "__main__":
    main()
