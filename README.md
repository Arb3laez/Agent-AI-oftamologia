# Sistema de Diagnóstico Oftalmológico Multi-Agente Cloud-Native

Este proyecto ha sido migrado a una arquitectura de microservicios escalable, diseñada para desplegarse en Kubernetes y utilizando modelos de IA de Groq.

## 🏗 Arquitectura

El sistema se compone de los siguientes microservicios:

- **Orquestador (Orchestrator)**: API Gateway y coordinador del flujo de diagnóstico. Expone endpoints REST y gestiona la comunicación.
- **Servicios de Agentes**:
  - `agent-general`: Oftalmología General.
  - `agent-retina`: Especialista en Retina.
  - `agent-cornea`: Especialista en Córnea.
  - `agent-neuro`: Neuro-oftalmología.
  - `agent-director`: Sintetiza los reportes y genera el diagnóstico final.
- **Infraestructura**:
  - Redis: Caché y Rate Limiting.
  - Prometheus/Grafana: Observabilidad.

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker & Docker Compose
- Python 3.11+
- Clave de API de Groq en `.env`

### Configuración Local

1.  **Validar API de Groq**:
    ```bash
    python scripts/validate_groq.py
    ```

2.  **Levantar el entorno local**:
    ```bash
    docker-compose up --build
    ```
    El orquestador estará disponible en `http://localhost:8000`.
    Grafana en `http://localhost:3000`.

### Uso de la API

Endpoint: `POST /diagnose`

```json
{
  "historial": "Paciente masculino de 45 años con visión borrosa..."
}
```

## ☸️ Despliegue en Kubernetes

Los manifiestos se encuentran en `infrastructure/k8s`.

```bash
kubectl apply -f infrastructure/k8s/orchestrator/
kubectl apply -f infrastructure/k8s/agents/
```

## 🛠 Desarrollo

- **Estructura**:
    - `orchestrator/`: Código del orquestador.
    - `agents/`: Código de los agentes (compartido).
    - `agents/Utils/`: Lógica de negocio y prompts.
    - `scripts/`: Scripts de utilidad.
- **Testing**:
    Ejecutar `pytest` para correr las pruebas.

## 🔒 Seguridad

- Las API Keys se manejan como Secretos de Kubernetes (`groq-secrets`).
- Comunicación interna vía HTTP (puede mejorarse a gRPC o mTLS).
- Análisis de vulnerabilidades con Bandit en CI/CD.
