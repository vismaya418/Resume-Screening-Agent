import fitz
import docx

def extract_text(file_path):

    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx(file_path)

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    return ""


def extract_pdf(file_path):

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text


def extract_docx(file_path):

    doc = docx.Document(file_path)

    return "\n".join(
        p.text for p in doc.paragraphs
    )