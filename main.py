import os
from typing import List
from dotenv import load_dotenv
from load_doc import load_resume
from chunk_doc import chunk_document
from embed_doc import store_documents
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# =========================
# Environment Setup
# =========================
load_dotenv()  # Load OPENAI_API_KEY from .env

# =========================
# Job Description (Query)
# =========================
JOB_DESCRIPTION = """
Position: Senior Python Developer (AI Integration)

RESPONSIBILITIES:
- Design and maintain high-performance backends using FastAPI.
- Implement machine learning models, specifically Transformers and NLP pipelines.
- Optimize database queries and manage vector data.

REQUIREMENTS:
- Minimum 3 years of experience in Python development.
- Strong understanding of Pydantic and asynchronous programming.
- Experience with Docker and cloud deployment.
"""

# =========================
# Prompt Template
# =========================
PROMPT = ChatPromptTemplate.from_template("""
You are a resume analysis assistant.

Use ONLY the context below to answer the question.
If the context does NOT contain relevant information, say "Not relevant".

Context:
{context}

Question:
{question}

Answer:
""")

# =========================
# Helper: Format Documents
# =========================
def format_documents(docs) -> str:
    """
    Convert retrieved LangChain Documents into a single text block
    for the LLM prompt context.
    """
    return "\n\n".join(doc.page_content for doc in docs)

# =========================
# Main Application Logic
# =========================
def main():
    print("🚀 Starting the job posting agent...")

    # ---- Load Resume ----
    resume_docs = load_resume("PARTH PATEL.pdf")
    print(f"📄 Loaded {len(resume_docs)} document(s) from resume.")

    # ---- Chunk Resume ----
    chunks = chunk_document(resume_docs)
    print(f"✂️ Chunked resume into {len(chunks)} pieces.")

    # ---- Store in Vector Store ----
    vector_store = store_documents(chunks)
    print("📦 Stored resume chunks in vector store.")

    # ---- Create Retriever ----
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    # ---- Retrieve Relevant Context ----
    retrieved_docs = retriever.invoke(JOB_DESCRIPTION)
    context = format_documents(retrieved_docs)
    print("🔍 Retrieved relevant resume context.")

    # ---- Build Prompt ----
    prompt_message = PROMPT.format_prompt(
        context=context,
        question='Is the candidate a good fit for this role?'
    )

    # ---- Initialize LLM ----
    llm = ChatOpenAI(
        model="gpt-5-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # ---- Generate Response ----
    response = llm.invoke(prompt_message)
    print("🧠 Generated response from LLM:\n")
    print(response.content)


# =========================
# Script Entry Point
# =========================
if __name__ == "__main__":
    main()
