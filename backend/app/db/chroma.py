# app/db/chroma.py
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from app.config import CHROMA_PERSIST_DIR, COLLECTION_NAME, OLLAMA_BASE_URL, EMBEDDING_MODEL

# 1. Inicializar el modelo de Embeddings local (Nomic Embed Text vía Ollama)
embeddings = OllamaEmbeddings(
    base_url=OLLAMA_BASE_URL,
    model=EMBEDDING_MODEL
)

def get_vector_store() -> Chroma:
    """
    Retorna la instancia de la base de datos vectorial ChromaDB.
    """
    return Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

def get_retriever(k: int = 3):
    """
    Retorna el recuperador (retriever) para buscar los k fragmentos más relevantes.
    """
    vector_store = get_vector_store()
    return vector_store.as_retriever(search_kwargs={"k": k})