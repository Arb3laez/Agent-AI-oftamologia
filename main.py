"""
Script Principal: main.py
Descripción: Orquesta el flujo de trabajo de los agentes de IA para el diagnóstico oftalmológico.
Idioma: Español
"""

import os
import sys
import sys
from dotenv import load_dotenv # type: ignore
from Utils.cliente_gemini import ClienteGemini
from Utils.agentes import (
    AgenteOftalmologoGeneral,
    AgenteRetina,
    AgenteCornea,
    AgenteNeuroOftalmologia,
    EquipoMultidisciplinarioOftalmologico
)

# Cargar variables de entorno desde .env al inicio
load_dotenv()

def leer_historial(ruta_archivo):
    """Lee el contenido del archivo de historial clínico."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo: {ruta_archivo}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

def guardar_resultado(contenido, ruta_salida):
    """Guarda el resultado final en un archivo."""
    try:
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"\n[ÉXITO] Diagnóstico guardado en: {ruta_salida}")
    except Exception as e:
        print(f"Error al guardar el resultado: {e}")

def main():
    print("=== INICIANDO SISTEMA DE AGENTES OFTALMOLÓGICOS ===")
    
    # 1. Configuración
    # Busca la API KEY en variable de entorno
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\n[ERROR] No se detectó la variable de entorno GEMINI_API_KEY.")
        # Opcional: Pedir input manual si no está en env
        print("Por favor, configura la variable o ingresala a continuación (no se guardará):")
        api_key = input("API Key: ").strip()
        if not api_key:
            print("Saliendo...")
            sys.exit(1)

    # 2. Inicializar Cliente y Agentes
    try:
        cliente = ClienteGemini(api_key=api_key)
        
        agentes = [
            AgenteOftalmologoGeneral(cliente),
            AgenteRetina(cliente),
            AgenteCornea(cliente),
            AgenteNeuroOftalmologia(cliente)
        ]
        
        director = EquipoMultidisciplinarioOftalmologico(cliente)
    except Exception as e:
        print(f"Error al inicializar agentes: {e}")
        sys.exit(1)

    # 3. Leer Historial Clínico
    ruta_historial = os.path.join("Historales_Oftalmologicos", "Reporte - Juan Perez - Vision Borrosa.txt")
    print(f"\nLeyendo historial clínico de: {ruta_historial}...")
    historial = leer_historial(ruta_historial)

    # 4. Ciclo de Análisis de Agentes
    reportes_generados = {}
    
    print("\n--- INICIANDO RODA DE CONSULTAS CON ESPECIALISTAS ---\n")
    
    for agente in agentes:
        print(f"> Consultando con {agente.nombre} ({agente.especialidad})...")
        respuesta = agente.analizar(historial)
        reportes_generados[agente.especialidad] = respuesta
        print(f"  Perfecto ! Reporte recibido.")

    # 5. Integración Final
    print("\n--- GENERANDO CONSENSO MÉDICO FINAL ---\n")
    diagnostico_final = director.analizar_reportes(historial, reportes_generados)

    # 6. Guardar Resultados
    ruta_salida = os.path.join("resultados", "diagnostico_final.txt")
    guardar_resultado(diagnostico_final, ruta_salida)
    
    print("\n=== PROCESO COMPLETADO CON ÉXITO ===")

if __name__ == "__main__":
    main()
