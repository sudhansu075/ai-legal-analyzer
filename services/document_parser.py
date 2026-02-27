from pypdf import PdfReader
from docx import Document
from PIL import Image
import pytesseract


def parse_document(file, filename: str):

    extension = filename.split(".")[-1].lower()

    if extension == "pdf":
        return parse_pdf(file)

    elif extension == "docx":
        return parse_docx(file)

    elif extension == "txt":
        return parse_txt(file)

    elif extension in ["png", "jpg", "jpeg"]:
        return parse_image(file)

    else:
        raise ValueError("Unsupported file format")


def parse_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"
    return text


def parse_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


def parse_txt(file):
    return file.read().decode("utf-8")


def parse_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)