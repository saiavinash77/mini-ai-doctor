from pypdf import PdfReader,PdfWriter
from typing import List,Optional
from io import BytesIO

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or " ")
    return "\n".join(texts)

# def extract_text_from_pdf(pdf):
#     reader = PdfReader(pdf)
#     text = [page.extract_text() or " " for page in reader.pages]
#     return "\n".join(text)