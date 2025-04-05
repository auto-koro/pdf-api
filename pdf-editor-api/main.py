from fastapi import FastAPI
from pydantic import BaseModel
import fitz  # PyMuPDF
import requests

app = FastAPI()

class PDFRequest(BaseModel):
    pdf_url: str
    image_url: str | None = None
    text: str

@app.post("/edit-pdf")
def edit_pdf(data: PDFRequest):
    pdf_path = "input.pdf"
    output_path = "output.pdf"

    with open(pdf_path, "wb") as f:
        f.write(requests.get(data.pdf_url).content)

    doc = fitz.open(pdf_path)
    page = doc[0]
    page.insert_text((100, 100), data.text, fontsize=14)

    if data.image_url:
        image_path = "image.png"
        with open(image_path, "wb") as f:
            f.write(requests.get(data.image_url).content)
        rect = fitz.Rect(100, 150, 300, 250)
        page.insert_image(rect, filename=image_path)

    doc.save(output_path)
    doc.close()

    return {"message": "PDF created"}
