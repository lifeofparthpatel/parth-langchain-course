from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_document(documents, chunk_size=500, chunk_overlap=50):
    """
    Chunk the given documents into smaller pieces.
    
    Args:
        documents (List[Document]): The list of documents to be chunked.
        chunk_size (int): The size of each chunk.
        chunk_overlap (int): The overlap between chunks.
    
    Returns:
        List[Document]: The list of chunked documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    return chunks