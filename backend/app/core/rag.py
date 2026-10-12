# app/core/rag.py
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.config import OLLAMA_BASE_URL, LLM_MODEL
from app.core.prompts import EASY_READ_PROMPT
from app.db.chroma import get_retriever

# 1. Inicializar el LLM local (Mistral) vía Ollama
llm = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model=LLM_MODEL,
    temperature=0.2  # Temperatura baja para respuestas consistentes y sin alucinaciones
)

def format_docs(docs):
    """
    Formatea los documentos recuperados concatenando sus textos.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    """
    Construye y retorna la cadena RAG accesible.
    """
    retriever = get_retriever(k=3)
    
    # Cadena LCEL: Recuperar contexto -> Formatear -> Aplicar Prompt -> LLM -> Parsear a String
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | EASY_READ_PROMPT
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

def answer_question(question: str) -> str:
    """
    Función de alto nivel para procesar una pregunta y devolver la respuesta adaptada.
    """
    chain = get_rag_chain()
    return chain.invoke(question)