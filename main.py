import os
from typing import List
from dotenv import load_dotenv 
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from load_doc import load_resume
# =========================
# Environment Setup
# =========================
load_dotenv()


# =========================
# Main Entry Point
# =========================
def main():
    print("Starting the job posting agent...")
    doc = load_resume("PARTH PATEL.pdf")
    print(f"Loaded {len(doc)} documents from the resume.")
# =========================
# Script Execution Guard
# =========================
if __name__ == "__main__":
    main()