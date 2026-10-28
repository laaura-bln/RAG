import os
import shutil
import tempfile
import pandas as pd
from fastapi import FastAPI, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import HOST, PORT
from app.core.rag import answer_question
from pipeline.run_ingest import load_web_documents, get_vector_store, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

app = FastAPI(
    title="ANTICIPA API",
    description="Backend RAG adaptado a Lectura Fácil para accesibilidad cognitiva.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

class IngestRequest(BaseModel):
    url: str

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok", "service": "ANTICIPA API"}

@app.post("/api/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pregunta no puede estar vacía."
        )
    try:
        response_text = answer_question(request.question)
        return AnswerResponse(answer=response_text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando la consulta: {str(e)}"
        )

@app.post("/api/ingest-url")
async def ingest_url(request: IngestRequest):
    try:
        docs = load_web_documents([request.url])
        if not docs:
            return {"status": "error", "message": "No se pudo extraer contenido de la URL."}

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)

        vector_store = get_vector_store()
        vector_store.add_documents(chunks)

        return {"status": "success", "message": f"URL ingerida con éxito ({len(chunks)} fragmentos)."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/ingest-pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"status": "error", "message": "El archivo debe ser un PDF válido."}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name

    try:
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)

        vector_store = get_vector_store()
        vector_store.add_documents(chunks)

        return {"status": "success", "message": f"PDF '{file.filename}' ingerido con éxito ({len(chunks)} fragmentos)."}
    except Exception as e:
        return {"status": "error", "message": f"Error al procesar el PDF: {str(e)}"}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.post("/api/ingest-excel")
async def ingest_excel(file: UploadFile = File(...)):
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
        return {"status": "error", "message": "El archivo debe ser un Excel (.xlsx o .xls)."}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name

    try:
        excel_data = pd.read_excel(tmp_path, sheet_name=None)
        docs = []

        for sheet_name, df in excel_data.items():
            text_content = f"Hoja: {sheet_name}\n" + df.to_string(index=False)
            docs.append(Document(
                page_content=text_content,
                metadata={"source": file.filename, "sheet": sheet_name}
            ))

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)

        vector_store = get_vector_store()
        vector_store.add_documents(chunks)

        return {"status": "success", "message": f"Excel '{file.filename}' ingerido con éxito ({len(chunks)} fragmentos)."}
    except Exception as e:
        return {"status": "error", "message": f"Error al procesar el Excel: {str(e)}"}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)