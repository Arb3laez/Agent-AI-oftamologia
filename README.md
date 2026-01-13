# Sistema de Agentes de IA para Diagnóstico Oftalmológico 👁️🩺

Este proyecto implementa una arquitectura de **Agentes de IA Multi-rol** especializados en oftalmología. Utiliza el modelo **Gemini 2.0 Flash** de Google para analizar historiales clínicos en texto y simular una junta médica de especialistas.

> **Nota**: Este sistema es una herramienta experimental y educativa. NO sustituye el juicio médico profesional real.

## 🚀 Características


- **Arquitectura Modular**: Agentes independientes para cada subespecialidad.
- **Integración Inteligente**: Un agente "Director Médico" sintetiza los hallazgos.
- **Entrada/Salida**: Procesa archivos `.txt` y genera informes detallados.

## 👥 Los Agentes Especialistas

El sistema cuenta con un equipo médico virtual compuesto por:

1.  **Dr. General (Oftalmología General)**:
    - Evalúa agudeza visual, presión intraocular y antecedentes sistémicos.
2.  **Dra. Retina (Retina y Vítreo)**:
    - Experta en fondo de ojo, retinopatía diabética y desprendimientos.
3.  **Dr. Córnea (Córnea y Superficie)**:
    - Analiza segmento anterior, infecciones y queratopatías.
4.  **Dra. Neuro (Neuro-Oftalmología)**:
    - Revisa nervio óptico, campos visuales y conexión cerebro-ojo.
5.  **Director Médico (Equipo Multidisciplinario)**:
    - Recibe todos los reportes, resuelve contradicciones y emite el diagnóstico final.

## 🛠️ Requisitos e Instalación

### Prerrequisitos
- Python 3.9 o superior.
- Una API Key de Google Gemini (Google AI Studio).

### Instalación

1.  **Clonar o descargar el proyecto**:
    Asegúrate de tener la carpeta `Agent-AI-oftalmología`.

2.  **Instalar dependencias**:
    Necesitas la librería `google-generativeai`. Ejecuta en tu terminal:
    ```bash
    pip install google-generativeai python-dotenv
    ```

## ⚙️ Configuración

Este sistema requiere una **API Key de Gemini** para funcionar.

### Opción A: Variable de Entorno (Recomendada)
Configura la variable `GEMINI_API_KEY` en tu sistema operativo.

**En Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="TU_API_KEY_AQUI"
```

**En Linux/Mac:**
```bash
export GEMINI_API_KEY="TU_API_KEY_AQUI"
```

### Opción B: Ingreso Manual
Si no configuras la variable, el sistema te pedirá la clave al ejecutarlo.

## ▶️ Ejecución

1.  Asegúrate de tener un historial clínico en la carpeta `Historales_Oftalmologicos`. Ya incluimos uno de ejemplo: `Reporte - Juan Perez - Vision Borrosa.txt`.
2.  Ejecuta el script principal desde la raíz del proyecto:

```bash
python main.py
```

3.  Observa el progreso en la consola mientras los agentes "piensan".
4.  Al finalizar, busca tu reporte en:
    `resultados/diagnostico_final.txt`

## 📂 Estructura del Proyecto

```
Agent-AI-oftalmología/
├── Historales_Oftalmologicos/ 
├── Utils/
│   ├── agentes.py             
│   └── cliente_gemini.py      
├── resultados/                 
├── main.py                  
└── README.md                  
```

