from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import logging

# Локальные импорты
from extractor import extract_text as extract_pdf_image
from utils.chunker import split_text_into_chunks
from embeddings.embedder import get_embeddings
from vector_db.db_manager import VectorDBManager

# Для .docx
from docx import Document

app = FastAPI(
    title="Document RAG API",
    description="API для извлечения, индексации и поиска по содержимому документов (PDF, JPG, PNG, DOCX, TXT)",
    version="1.0.0"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)

# Инициализируем менеджер БД
db_manager = VectorDBManager()

# -----------------------------------------------
# Универсальная функция извлечения текста
# -----------------------------------------------

def extract_text_from_file(file_path):
    """
    Извлекает текст из файла на основе его расширения.
    Поддерживает: PDF, JPG, PNG, DOCX, TXT
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf" or ext in [".jpg", ".jpeg", ".png"]:
        # Используем существующий extractor.py
        return extract_pdf_image(file_path)

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        raise ValueError(f"Unsupported file format: {ext}")

# -----------------------------------------------
# API Эндпоинты
# -----------------------------------------------

@app.post("/ai-tools/extract-text/", tags=["Document Management"])
async def extract_text_endpoint(file: UploadFile = File(...)):
    """
    Загружает файл (PDF, JPG, PNG, DOCX, TXT), извлекает текст и сохраняет его в векторную БД.
    """
    logging.info(f"Received file: {file.filename}")
    try:
        # 1. Сохраняем файл
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 2. Извлекаем текст
        extracted_text = extract_text_from_file(file_path)

        # 3. Разбиваем на чанки
        chunks = split_text_into_chunks(extracted_text)

        # 4. Сохраняем в ChromaDB
        db_manager.add_document(file.filename, chunks)

        # 5. Удаляем временный файл
        os.remove(file_path)

        return JSONResponse(content={
            "text_preview": extracted_text[:500],
            "chunks_added": len(chunks),
            "filename": file.filename
        })
    except Exception as e:
        logging.error(f"Error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/ai-tools/search/", tags=["Search"])
async def search_query(q: str):
    """
    Выполняет поиск по запросу q и возвращает ближайшие фрагменты текста.
    """
    results = db_manager.search(q)
    return {"query": q, "results": results}


@app.delete("/ai-tools/delete/", tags=["Document Management"])
async def delete_document(source: str):
    """
    Удаляет все фрагменты, связанные с указанным документом (по имени файла).
    """
    try:
        db_manager.delete_document(source)
        return {"status": "success", "message": f"Document '{source}' deleted from database"}
    except Exception as e:
        logging.error(f"Error deleting document: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})