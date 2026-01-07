from typing import List
from pydantic import BaseModel, Field

class JobPosting(BaseModel):
    """Schema for a source used by a agent."""

    url:str = Field(description="The URL of the source.")

class AgentResponse(BaseModel):
    """Schema for agent response."""

    answer:str = Field(description="The agent's answer to the query")
    source:List[JobPosting] = Field(default_factory=list, description="List of sources used to generate the answer.")
