import fitz

# Fitz is the PyMuPDF library used for PDF processing
def load_pdf(file_path):
    file_bytes = file_path.file.read()

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""

    for page in doc:
        text += page.get_text()

    return text