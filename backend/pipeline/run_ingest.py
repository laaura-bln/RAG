# pipeline/run_ingest.py
import os
os.environ["USER_AGENT"] = "AnticipaBot/1.0"

from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.db.chroma import get_vector_store

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_local_documents() -> List[Document]:
    """Carga archivos PDF y TXT dentro de la carpeta /data."""
    documents = []
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Carpeta creada: {DATA_DIR}. Deposita aquí tus archivos PDF o TXT.")
        return documents

    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file)
        if file.endswith(".pdf"):
            print(f"Procesando PDF: {file}")
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif file.endswith(".txt"):
            print(f"Procesando TXT: {file}")
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())

    return documents

def load_web_documents(urls: List[str]) -> List[Document]:
    """Carga y limpia el contenido de una lista de páginas web."""
    documents = []
    if not urls:
        return documents

    print(f"Cargando {len(urls)} páginas web...")
    for url in urls:
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            documents.extend(docs)
            print(f"Página web cargada con éxito: {url}")
        except Exception as e:
            print(f"Error cargando la URL {url}: {e}")

    return documents

def run_ingestion():
    """Ejecuta la ingesta completa (PDF, TXT y Web) hacia ChromaDB."""
    all_docs = []
    
    local_docs = load_local_documents()
    all_docs.extend(local_docs)
    
    if not all_docs:
        print("No se encontraron documentos ni URLs para ingerir.")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(all_docs)
    print(f"Total de fragmentos (chunks) creados: {len(chunks)}")

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
    print("Ingesta completada con éxito en ChromaDB.")

if __name__ == "__main__":
    run_ingestion()