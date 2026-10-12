# pipeline/run_ingest.py
import sys
import os

# Añadir la raíz del proyecto al sys.path para poder importar módulos de 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.documents import Document
from app.db.chroma import get_vector_store

def run_ingestion():
    print("Iniciando la ingesta de documentos en ChromaDB (modo local)...")
    
    # 1. Documentos de prueba (simulando circulares y notas informativas)
    sample_documents = [
        Document(
            page_content=(
                "Excursión al Museo de Ciencias: El próximo viernes 20 de noviembre de 2026 "
                "iremos de excursión. La salida será a las 9:00 de la mañana desde la puerta principal "
                "del centro. Regresaremos a las 17:00 de la tarde. Es necesario llevar comida, agua "
                "y calzado cómodo."
            ),
            metadata={"fuente": "circular_01.pdf", "categoria": "excursiones"}
        ),
        Document(
            page_content=(
                "Cambio de horario en el taller de cocina: A partir de la semana que viene, "
                "el taller de cocina se impartirá los martes a las 11:00 de la mañana en lugar de los "
                "jueves. El taller tendrá lugar en el aula 3."
            ),
            metadata={"fuente": "nota_cocina.pdf", "categoria": "talleres"}
        ),
        Document(
            page_content=(
                "Norma sobre el menú del comedor: El menú especial de fruta fresca estará "
                "disponible todos los días al finalizar el almuerzo, a las 13:30."
            ),
            metadata={"fuente": "comedor_info.pdf", "categoria": "comedor"}
        )
    ]
    
    # 2. Conectar a ChromaDB e indexar los documentos
    vector_store = get_vector_store()
    
    print(f"Guardando {len(sample_documents)} documentos en la base de datos vectorial...")
    vector_store.add_documents(sample_documents)
    
    print("Ingesta completada con éxito. La base de datos local está lista.")

if __name__ == "__main__":
    run_ingestion()