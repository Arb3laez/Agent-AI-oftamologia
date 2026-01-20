"""
Cliente para API de Groq con patrones de resiliencia.
Incluye: Circuit Breaker, Retry Backoff, Caching (Redis), Rate Limiting handling.
"""

import os
import json
import hashlib
import time
from typing import Optional, Dict, Any, Generator
from groq import Groq, APIConnectionError, RateLimitError, APIStatusError
import redis
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import structlog
from datetime import timedelta

# Configuración de Logging
logger = structlog.get_logger()

class CircuitBreakerOpenException(Exception):
    pass

class ClienteGroq:
    """
    Cliente robusto para interactuar con la API de Groq.
    Implementa patrones de diseño para microservicios cloud-native.
    """
    
    def __init__(self, api_key: Optional[str] = None, redis_url: Optional[str] = None):
        """
        Inicializa el cliente de Groq mejorado.
        
        Args:
            api_key: API key de Groq.
            redis_url: URL de conexión a Redis para caché.
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Se requiere GROQ_API_KEY")
            
        self.client = Groq(api_key=self.api_key)
        
        # Redis para caché
        self.redis_url = redis_url or os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        self.cache_enabled = os.environ.get("ENABLE_CACHE", "true").lower() == "true"
        self.redis = None
        
        if self.cache_enabled:
            try:
                self.redis = redis.from_url(self.redis_url, decode_responses=True, socket_connect_timeout=1)
                self.redis.ping()
                logger.info("cache_connected", url=self.redis_url)
            except Exception as e:
                logger.warning("cache_connection_failed", error=str(e))
                self.redis = None # Fallback sin caché

        # Configuración de modelo
        self.modelo = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.max_tokens = int(os.environ.get("GROQ_MAX_TOKENS", 4096))
        self.temperature = float(os.environ.get("GROQ_TEMP", 0.7))

        # Circuit Breaker State (Simple implementation)
        self.failure_count = 0
        self.failure_threshold = 5
        self.reset_timeout = 60  # seconds
        self.last_failure_time = 0

    def _check_circuit_breaker(self):
        """Verifica si el circuito está abierto."""
        if self.failure_count >= self.failure_threshold:
            time_since_failure = time.time() - self.last_failure_time
            if time_since_failure < self.reset_timeout:
                raise CircuitBreakerOpenException(f"Circuit open. Retrying in {self.reset_timeout - time_since_failure:.0f}s")
            else:
                # Half-open: Permite intentar de nuevo
                self.failure_count = 0 

    def _get_cache_key(self, prompt: str, system_prompt: str, model: str) -> str:
        """Genera una clave única para caché basada en los inputs."""
        content = f"{prompt}|{system_prompt}|{model}"
        return f"groq:cache:{hashlib.sha256(content.encode()).hexdigest()}"

    @retry(
        retry=retry_if_exception_type((APIConnectionError, RateLimitError, APIStatusError)),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        before_sleep=before_sleep_log(logger, "warning")
    )
    def generar_respuesta(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Genera respuesta con retry, cache y circuit breaker.
        """
        self._check_circuit_breaker()
        
        system_prompt = system_prompt or ""
        
        # 1. Verificar Caché
        if self.redis:
            cache_key = self._get_cache_key(prompt, system_prompt, self.modelo)
            try:
                cached = self.redis.get(cache_key)
                if cached:
                    logger.info("cache_hit", key=cache_key)
                    return cached
            except Exception as e:
                logger.error("cache_read_error", error=str(e))

        # 2. Llamada a API
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            start_time = time.time()
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.modelo,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
            )
            duration = time.time() - start_time
            
            response_text = chat_completion.choices[0].message.content
            
            # Log metrics (podríamos pushear a prometheus aquí también)
            logger.info("groq_request_success", model=self.modelo, duration=duration, tokens=chat_completion.usage.total_tokens)

            # 3. Guardar en Caché (TTL 24h)
            if self.redis:
                try:
                    self.redis.setex(cache_key, timedelta(hours=24), response_text)
                except Exception as e:
                    logger.error("cache_write_error", error=str(e))

            self.failure_count = 0
            return response_text

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            logger.error("groq_request_failed", error=str(e), attempt=self.failure_count)
            raise
