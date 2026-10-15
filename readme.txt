Tecnologías Utilizadas

Backend y API
FastAPI: Framework web asíncrono de alto rendimiento escrito en Python.
Se encarga de levantar el servidor web y ofrecer la documentación interactiva Swagger.

Uvicorn: Servidor ASGI encargado de ejecutar la aplicación FastAPI y gestionar las peticiones en segundo plano.

Pydantic: Librería para la validación de datos y esquemas en Python. 
Asegura que los JSON recibidos y enviados cumplan con la estructura requerida.



IA Local y Motor RAG
Ollama: Servidor y motor de inferencia local. 
Permite ejecutar modelos de lenguaje pesados directamente en el ordenador sin depender de internet ni enviar datos
a servidores externos.

Mistral (vía Ollama): Modelo de lenguaje principal (LLM) de 7 billones de parámetros. 
Genera el texto final adaptado a Lectura Fácil a partir de la información recuperada.

Nomic-Embed-Text (vía Ollama): Modelo especializado en embeddings. Convierte textos
 (preguntas y fragmentos de documentos) en vectores numéricos de alta precisión semántica.

LangChain / LCEL: Framework de orquestación que encadena la lógica entre el retriever, las plantillas 
de prompts y los modelos de IA.



Almacenamiento e Ingesta de Datos
ChromaDB: Base de datos vectorial persistente. Almacena los fragmentos de texto representados como vectores
para hacer búsquedas por similitud semántica de forma instantánea.

PyPDF: Librería de Python para extraer y procesar texto plano a partir de archivos en formato PDF.

*Todo se puede descargar desde los requeriments menos ollama, hay que usar el comando ollama run mistral