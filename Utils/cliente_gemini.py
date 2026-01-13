"""
Módulo: cliente_gemini.py
Descripción: Gestiona la conexión con la API de Google Gemini para realizar consultas.
Idioma: Español
"""

import os
import google.generativeai as genai
from typing import Optional

class ClienteGemini:
    """
    Clase encargada de configurar y comunicar con el modelo Gemini.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de Gemini.
        Intenta obtener la API key de los argumentos o de las variables de entorno.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("No se encontró una API Key para Gemini. Configura la variable de entorno GEMINI_API_KEY o pásala al constructor.")

        genai.configure(api_key=self.api_key)
        
        # Configuración del modelo
        self.generation_config = {
            "temperature": 0.2, # Baja temperatura para diagnósticos más precisos y menos creativos
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        self.model_name = "gemini-2.0-flash" # Usando versión flash optimizada
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
        )

    def generar_respuesta(self, prompt: str) -> str:
        """
        Envía un prompt al modelo y retorna la respuesta en texto.
        
        Args:
            prompt (str): El texto con las instrucciones y datos para el modelo.
            
        Returns:
            str: La respuesta generada por el modelo.
        """
        try:
            chat_session = self.model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error al consultar a Gemini: {str(e)}"

# Prueba simple si se ejecuta directamente
if __name__ == "__main__":
    try:
        # Nota: Esto fallará si no hay API KEY configurada en el entorno
        cliente = ClienteGemini()
        print("Conexión exitosa. Probando modelo...")
        respuesta = cliente.generar_respuesta("Di 'Hola, sistema oftalmológico listo' en español.")
        print(respuesta)
    except Exception as e:
        print(f"Error en la prueba: {e}")
