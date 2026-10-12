# app/main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import HOST, PORT
from app.core.rag import answer_question

app = FastAPI(
    title="ANTICIPA API",
    description="Backend RAG adaptado a Lectura Fácil para accesibilidad cognitiva.",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde la PWA en React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se restringirá al dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquemas Pydantic para validación de entrada/salida
class QuestionRequest(BaseModel):
    question: str = Field(..., example="¿A qué hora sale la excursión del viernes?")

class AnswerResponse(BaseModel):
    answer: str

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Endpoint para verificar que el servidor está activo."""
    return {"status": "ok", "service": "ANTICIPA API"}

@app.post("/api/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    """
    Endpoint principal para enviar una pregunta al sistema RAG
    y recibir la respuesta en Lectura Fácil.
    """
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)