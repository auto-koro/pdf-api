from fastapi import FastAPI
from pydantic import BaseModel
import fitz
import requests
from fastapi.responses import JSONResponse
import uuid

app = FastAPI()

class PDFEditRequest(BaseModel):
    file_url: str
    customer_name: str
    insert_text: str
    image_url: str

@app.post("/pdf_edit")
def edit_pdf(req: PDFEditRequest):
    # PDFをダウンロード
    pdf_response = requests.get(req.file_url)
    pdf_path = f"{uuid.uuid4()}_original.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf_response.content)

    # PDFを開く
    doc = fitz.open(pdf_path)
    page = doc[0]

    # テキストを挿入（位置は要調整）
    text_position = fitz.Point(100, 100)
    page.insert_text(text_position, f"{req.customer_name} 様 {req.insert_text}",
                     fontsize=12, color=(0, 0, 0))

    # 画像をダウンロード
    image_response = requests.get(req.image_url)
    image_path = f"{uuid.uuid4()}_image.png"
    with open(image_path, "wb") as img_f:
        img_f.write(image_response.content)

    # 画像挿入（位置要調整）
    image_rect = fitz.Rect(100, 150, 300, 350)
    page.insert_image(image_rect, filename=image_path)

    # 編集後のPDFを保存
    output_pdf_path = f"{uuid.uuid4()}_edited.pdf"
    doc.save(output_pdf_path)
    doc.close()

    # PDFをどこかにアップロードする必要がある（例えばAWS S3, Google Cloud Storageなど）
    # 今回は仮にURLを「https://example.com/...」として返すことにします
    edited_pdf_url = f"https://example.com/{output_pdf_path}"

    # 最終的にレスポンスを返す
    return JSONResponse({"edited_pdf_url": edited_pdf_url})
