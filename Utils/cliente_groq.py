
from groq import Groq
import os
from typing import Optional

class ClienteGroq:
    """Cliente para interactuar con la API de Groq (100% gratis)."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de Groq.
        
        Args:
            api_key: API key de Groq. Si no se proporciona, busca en GROQ_API_KEY
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "Se requiere una API key. "
                "Configura GROQ_API_KEY en .env o pásala como parámetro"
            )
        
        self.cliente = Groq(api_key=self.api_key)
        
        # Configuración por defecto
        # Modelos disponibles:
        # - llama-3.3-70b-versatile (RECOMENDADO - mejor calidad)
        # - llama-3.1-8b-instant (más rápido)
        # - mixtral-8x7b-32768 (balanceado)
        self.modelo = "llama-3.3-70b-versatile"
        self.max_tokens = 4096
        self.temperatura = 0.7
    
    def generar_respuesta(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperatura: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Genera una respuesta usando Groq.
        
        Args:
            prompt: Texto de entrada/pregunta
            system_prompt: Prompt de sistema (instrucciones de comportamiento)
            temperatura: Creatividad (0.0-1.0). Por defecto 0.7
            max_tokens: Máximo de tokens a generar. Por defecto 4096
            
        Returns:
            str: Respuesta generada por el modelo
        """
        try:
            # Construir mensajes
            mensajes = []
            
            # Agregar system prompt si existe
            if system_prompt:
                mensajes.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Agregar prompt del usuario
            mensajes.append({
                "role": "user",
                "content": prompt
            })
            
            # Parámetros de la llamada
            params = {
                "model": self.modelo,
                "messages": mensajes,
                "temperature": temperatura or self.temperatura,
                "max_tokens": max_tokens or self.max_tokens,
            }
            
            # Llamar a la API
            respuesta = self.cliente.chat.completions.create(**params)
            
            # Extraer texto de la respuesta
            return respuesta.choices[0].message.content
            
        except Exception as e:
            print(f"Error al generar respuesta: {e}")
            raise
    
    def generar_respuesta_stream(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None
    ):
        """
        Genera respuesta en modo streaming (para respuestas largas).
        
        Yields:
            str: Fragmentos de texto conforme se generan
        """
        try:
            mensajes = []
            
            if system_prompt:
                mensajes.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            mensajes.append({
                "role": "user",
                "content": prompt
            })
            
            params = {
                "model": self.modelo,
                "messages": mensajes,
                "temperature": self.temperatura,
                "max_tokens": self.max_tokens,
                "stream": True
            }
            
            stream = self.cliente.chat.completions.create(**params)
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"Error en streaming: {e}")
            raise
    
    def cambiar_modelo(self, modelo: str):
        """
        Cambia el modelo a utilizar.
        
        Args:
            modelo: Nombre del modelo (llama-3.3-70b-versatile, llama-3.1-8b-instant, etc.)
        """
        modelos_disponibles = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "llama-3.1-70b-versatile"
        ]
        
        if modelo not in modelos_disponibles:
            print(f" Advertencia: Modelo '{modelo}' no está en la lista conocida")
            print(f"   Modelos disponibles: {', '.join(modelos_disponibles)}")
        
        self.modelo = modelo
        print(f"✓ Modelo cambiado a: {modelo}")
    
    def obtener_info_modelo(self) -> dict:
        """Retorna información del modelo actual."""
        return {
            "modelo": self.modelo,
            "max_tokens": self.max_tokens,
            "temperatura": self.temperatura
        }