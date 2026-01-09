import os
from dotenv import load_dotenv

from load_doc import load_resume
from chunk_doc import chunk_document
from embed_doc import store_documents

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# =========================
# Environment Setup
# =========================
load_dotenv()

# =========================
# Job Description
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
# Helper
# =========================
def format_documents(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

# =========================
# Main
# =========================
def main():
    print("🚀 Starting the job posting agent...")

    # ---- Load Resume ----
    resume_docs = load_resume("PARTH PATEL.pdf")
    print(f"📄 Loaded {len(resume_docs)} document(s).")

    # ---- Chunk ----
    chunks = chunk_document(resume_docs)
    print(f"✂️ Chunked into {len(chunks)} pieces.")

    # ---- Vector Store ----
    vector_store = store_documents(chunks)
    print("📦 Stored in vector store.")

    # ---- Retriever ----
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # ---- LLM ----
    llm = ChatOpenAI(
        model="gpt-5-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # ---- Chain (THIS IS THE KEY PART) ----
    rag_chain = (
        {
            "context": retriever | format_documents,
            "question": RunnablePassthrough()
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )

    # ---- Invoke ----
    result = rag_chain.invoke(
        "Is the candidate a good fit for this role?"
    )

    print("\n🧠 LLM Response:\n")
    print(result)

# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    main() 