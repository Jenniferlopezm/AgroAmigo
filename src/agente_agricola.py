import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import TavilySearchResults



load_dotenv()


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

template = """
Eres una IA especializada en recuperar información útil para campesinos colombianos. 
Proporciona la información de manera clara y concisa, con ejemplos prácticos relevantes 
para la agricultura en Colombia.

Organiza la información en forma de tabla o texto, según cuál sea la más clara para la respuesta dada.

Usa solo el contexto proporcionado y la información obtenida en línea. No inventes información.

consulta: {pregunta}

Importante: Las respuestas deben estar solamente en ESPAÑOL. Además, solo debes limitarte a responder 
preguntas sobre el contexto de los campesinos colombianos. En el caso de que la pregunta se salga de este 
contexto, debes decir: "Lo siento, no puedo ayudarte. ¿Tienes otra pregunta?". La respuesta debe ser en Markdown.

{contexto}
"""

template_reformulacion = """
Eres una IA diseñada para mejorar la claridad y precisión de las preguntas de los usuarios para optimizar 
su búsqueda de información con Tavily. 

Toma la pregunta original del usuario y reformúlala de manera que sea más específica 
y fácil de entender. Asegúrate de incluir palabras clave relevantes y evitar ambigüedades.
 La nueva pregunta debe facilitar la obtención de información útil y concreta. Incluye para el Campo Colombiano

Pregunta original: {pregunta_usuario}

IMPORTANTE: Solo debes retornar la pregunta reformulada
"""

prompt = ChatPromptTemplate.from_template(template)

prompt_reformulación = ChatPromptTemplate.from_template(template_reformulacion)

class AgenteAgricola:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        ) 
        self.internet = TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            include_images=True
        )
        

    def preguntar(self,pregunta):

        #Afinar pregunta del usuario y generar nueva pregunta
        prompt_reformulación_completo = prompt_reformulación.format(pregunta_usuario=pregunta)
        pregunta_nueva = self.llm.invoke(prompt_reformulación_completo)
        
        # Buscar en Internet información de la pregunta reformulada del usario
        contexto_ = self.internet.invoke({"query": pregunta_nueva.content})
        
        # Con la información suministrada en el contexto, crear la salida
        prompt_completo = prompt.format(contexto=contexto_,pregunta=pregunta)
        respuesta = self.llm.invoke(prompt_completo)
        
        return respuesta.content
        
    