from langchain_community.document_loaders import TextLoader, PyMuPDFLoader

def load_resume(file_path: str):
    """
    Load a resume document from the given file path.
    
    Args:
        file_path (str): The path to the resume file.
    """

    if file_path.lower().endswith('.pdf'):
        loader = PyMuPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    
    documents = loader.load()
    return documents