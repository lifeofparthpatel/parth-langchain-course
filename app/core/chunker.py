from langchain_core.documents import Document

def chunk_resume(text: str):
    return [Document(page_content=text)]
