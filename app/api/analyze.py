from urllib import response
from fastapi import APIRouter, UploadFile, Form
from typing import List

from app.core.pdf_loader import load_pdf
from app.core.chunker import chunk_resume
from app.core.vector_store import store_documents
from app.agent.resume_agent import build_resume_agent
from app.llm.prompt import EVALUATION_PROMPT

router = APIRouter()

@router.post("/analyze")
async def analyze_resumes(
    resumes: List[UploadFile],
    job_description: str = Form(...)
):
    agent = build_resume_agent()
    results = []

    for resume in resumes:
        resume_text = load_pdf(resume)
        print("RESUME TEXT:", resume_text)
        chunks = chunk_resume(resume_text)
        print(f"Chunked into {len(chunks)} parts")
        vector_store = store_documents(chunks)
        print("Vector store created with embeddings")
        retriever = vector_store.as_retriever()

        relevant = retriever.invoke(job_description)
        context = "\n".join(d.page_content for d in relevant)
        print("RELEVANT CONTEXT:", context)
        response = agent.invoke({
            "job_description": job_description,
            "resume_text": context
        })


        print("RAW AGENT RESPONSE:", response)

        # # Tool output is stored in messages
        # tool_result = None
        # for msg in response["messages"]:
        #     if msg.type == "tool":
        #         tool_result = msg.content

        # if tool_result is None:
        #     raise RuntimeError("Agent did not call calculate_fit tool")

        # if tool_result["verdict"] != "Not suitable":
        #     results.append(tool_result)

    return results
