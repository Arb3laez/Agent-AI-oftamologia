
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Importar cliente y agentes
from Utils.cliente_groq import ClienteGroq
from Utils.agentes import (
    AgenteOftalmologoGeneral,
    AgenteRetina,
    AgenteCornea,
    AgenteNeuroOftalmologia,
    EquipoMultidisciplinarioOftalmologico
)

# Cargar variables de entorno
load_dotenv()

def imprimir_banner():
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                                                                      ║ 
║                                                                      ║ 
║      SISTEMA DE DIAGNÓSTICO OFTALMOLÓGICO MULTI-AGENTE               ║
║                                                                      ║
║                                                                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def leer_historial(ruta_archivo: str) -> str:
    """
    Lee el contenido del archivo de historial clínico.
    
    Args:
        ruta_archivo: Ruta al archivo de historial
        
    Returns:
        str: Contenido del historial
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        print(f"✓ Historial cargado: {os.path.basename(ruta_archivo)}")
        print(f"  Tamaño: {len(contenido)} caracteres\n")
        return contenido
    except FileNotFoundError:
        print(f"✗ Error: No se encontró el archivo: {ruta_archivo}")
        print(f"\n💡 Asegúrate de que el archivo existe en:")
        print(f"   {os.path.abspath(ruta_archivo)}\n")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error al leer el archivo: {e}")
        sys.exit(1)

def guardar_resultado(contenido: str, ruta_salida: str):
    """
    Guarda el resultado final en un archivo con timestamp.
    
    Args:
        contenido: Contenido a guardar
        ruta_salida: Ruta del archivo de salida
    """
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        
        # Agregar timestamp al nombre
        nombre_base, extension = os.path.splitext(ruta_salida)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_con_timestamp = f"{nombre_base}_{timestamp}{extension}"
        
        # Guardar archivo
        with open(ruta_con_timestamp, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"\n{'='*70}")
        print(f"✓ DIAGNÓSTICO GUARDADO EXITOSAMENTE")
        print(f"  📄 Archivo: {ruta_con_timestamp}")
        print(f"  📊 Tamaño: {len(contenido):,} caracteres")
        print(f"{'='*70}\n")
        
        return ruta_con_timestamp
        
    except Exception as e:
        print(f"✗ Error al guardar el resultado: {e}")
        return None

def mostrar_progreso(paso: int, total: int, descripcion: str):
    """Muestra barra de progreso."""
    porcentaje = (paso / total) * 100
    bloques_completos = int(porcentaje // 5)
    barra = "█" * bloques_completos + "░" * (20 - bloques_completos)
    print(f"[{barra}] {porcentaje:.0f}% - {descripcion}")

def verificar_api_key() -> str:
    """Verifica y obtiene la API key."""
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("="*70)
        print("⚠️  NO SE DETECTÓ LA API KEY DE GROQ")
        print("="*70)
        print("\n📝 Para configurar tu API key:\n")
        print("1. Ve a: https://console.groq.com/")
        print("2. Crea una cuenta (es gratis)")
        print("3. Genera una API key")
        print("4. Agrégala a tu archivo .env:\n")
        print("   GROQ_API_KEY=gsk_tu_api_key_aqui\n")
        print("-"*70)
        print("\n🔧 O ingrésala ahora (no se guardará):\n")
        
        api_key = input("API Key de Groq: ").strip()
        
        if not api_key:
            print("\n✗ No se proporcionó API key. Saliendo...")
            sys.exit(1)
        
        if not api_key.startswith("gsk_"):
            print("\n⚠️  Advertencia: La API key de Groq suele comenzar con 'gsk_'")
            continuar = input("¿Continuar de todos modos? (s/n): ").lower()
            if continuar != 's':
                sys.exit(1)
    else:
        # Mostrar API key parcialmente oculta
        print(f"✓ API key detectada: {api_key[:8]}...{api_key[-4:]}")
    
    return api_key

def main():
    """Función principal del sistema."""
    
    # Banner
    imprimir_banner()
    
    # ========================================
    # PASO 1: CONFIGURACIÓN DE API
    # ========================================
    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│ PASO 1: Configuración de API                                        │")
    print("└─────────────────────────────────────────────────────────────────────┘\n")
    
    api_key = verificar_api_key()
    
    # ========================================
    # PASO 2: INICIALIZACIÓN DE AGENTES
    # ========================================
    print("\n┌─────────────────────────────────────────────────────────────────────┐")
    print("│ PASO 2: Inicializando Sistema de Agentes                            │")
    print("└─────────────────────────────────────────────────────────────────────┘\n")
    
    try:
        # Crear cliente
        cliente = ClienteGroq(api_key=api_key)
        print(f"✓ Cliente Groq inicializado")
        print(f"  Modelo: {cliente.modelo}")
        print(f"  Límite: 14,400 requests/día\n")
        
        # Crear agentes especialistas
        agentes = [
            AgenteOftalmologoGeneral(cliente),
            AgenteRetina(cliente),
            AgenteCornea(cliente),
            AgenteNeuroOftalmologia(cliente)
        ]
        print(f"✓ {len(agentes)} agentes especialistas creados:")
        for agente in agentes:
            print(f"  • {agente.nombre} ({agente.especialidad})")
        
        # Crear director de equipo
        director = EquipoMultidisciplinarioOftalmologico(cliente)
        print(f"\n✓ Director del equipo médico inicializado")
        
    except Exception as e:
        print(f"\n✗ Error al inicializar agentes: {e}")
        print("\n💡 Posibles causas:")
        print("  • API key inválida")
        print("  • Sin conexión a internet")
        print("  • Límite de rate excedido\n")
        sys.exit(1)
    
    # ========================================
    # PASO 3: CARGA DE HISTORIAL CLÍNICO
    # ========================================
    print("\n┌─────────────────────────────────────────────────────────────────────┐")
    print("│ PASO 3: Carga de Historial Clínico                                  │")
    print("└─────────────────────────────────────────────────────────────────────┘\n")
    
    ruta_historial = os.path.join(
        "Historales_Oftalmologicos", 
        "Reporte - Steve Rogers - Vision Borrosa.txt"
    )
    
    historial = leer_historial(ruta_historial)
    
    # ========================================
    # PASO 4: CONSULTA CON ESPECIALISTAS
    # ========================================
    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│ PASO 4: Consulta con Especialistas                                  │")
    print("└─────────────────────────────────────────────────────────────────────┘\n")
    print(" Iniciando ronda de evaluaciones médicas...\n")
    
    reportes_generados = {}
    total_agentes = len(agentes)
    
    for idx, agente in enumerate(agentes, 1):
        print(f"\n{'─'*70}")
        mostrar_progreso(idx, total_agentes, f"{agente.nombre}")
        print(f"{'─'*70}")
        
        try:
            respuesta = agente.analizar(historial)
            reportes_generados[agente.especialidad] = respuesta
            print(f"  ✓ Reporte recibido ({len(respuesta)} caracteres)")
            
        except Exception as e:
            print(f"  ✗ Error en {agente.nombre}: {e}")
            print(f"    Continuando con otros especialistas...")
            continue
    
    # Verificar que tengamos al menos un reporte
    if not reportes_generados:
        print("\n✗ ERROR CRÍTICO: No se generó ningún reporte")
        print("  Verifica tu conexión y API key")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"✓ Evaluaciones completadas: {len(reportes_generados)}/{total_agentes}")
    print(f"{'='*70}")
    
    # ========================================
    # PASO 5: GENERACIÓN DE CONSENSO FINAL
    # ========================================
    print("\n┌─────────────────────────────────────────────────────────────────────┐")
    print("│ PASO 5: Generación de Consenso Médico Final                         │")
    print("└─────────────────────────────────────────────────────────────────────┘\n")
    print(" Integrando reportes de especialistas...\n")
    
    try:
        diagnostico_final = director.analizar_reportes(historial, reportes_generados)
        print("✓ Consenso médico generado exitosamente")
        print(f"  Extensión: {len(diagnostico_final):,} caracteres")
        
    except Exception as e:
        print(f"\n✗ Error al generar consenso: {e}")
        sys.exit(1)
    
    # ========================================
    # PASO 6: GUARDAR RESULTADOS
    # ========================================
    print("\n┌─────────────────────────────────────────────────────────────────────┐")
    print("│ PASO 6: Guardando Resultados                                        │")
    print("└─────────────────────────────────────────────────────────────────────┘")
    
    # Agregar metadata al inicio del documento
    metadata = f"""{'='*70}
DIAGNÓSTICO OFTALMOLÓGICO - REPORTE FINAL
{'='*70}
Fecha de generación: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
Sistema: Multi-Agente Oftalmológico
Modelo de IA: Groq - {cliente.modelo}
Especialistas consultados: {len(reportes_generados)}
{'='*70}

"""
    
    contenido_completo = metadata + diagnostico_final
    
    ruta_salida = os.path.join("resultados", "diagnostico_final.txt")
    archivo_guardado = guardar_resultado(contenido_completo, ruta_salida)
    
    # ========================================
    # RESUMEN FINAL
    # ========================================
    if archivo_guardado:
        print("╔══════════════════════════════════════════════════════════════════════╗")
        print("║                   ✓ PROCESO COMPLETADO EXITOSAMENTE                  ║")
        print("╚══════════════════════════════════════════════════════════════════════╝\n")
        
        print("RESUMEN:")
        print(f"  • Historial analizado: {os.path.basename(ruta_historial)}")
        print(f"  • Especialistas consultados: {len(reportes_generados)}/{total_agentes}")
        print(f"  • Diagnóstico guardado en: {archivo_guardado}\n")
        
        print(" PRÓXIMOS PASOS:")
        print("  1. Revisar el diagnóstico final")
        print("  2. Validar con médico tratante")
        print("  3. Implementar plan de manejo recomendado")
        print("  4. Programar seguimiento según indicaciones\n")
        
        print("  RECORDATORIO:")
        print("  Este diagnóstico es una herramienta de apoyo.")
        print("  Siempre debe ser validado por un profesional médico.\n")
    else:
        print("╔══════════════════════════════════════════════════════════════════════╗")
        print("║                   PROCESO COMPLETADO CON ADVERTENCIAS                 ║")
        print("╚══════════════════════════════════════════════════════════════════════╝\n")
        print("El diagnóstico se generó pero hubo problemas al guardarlo.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n╔══════════════════════════════════════════════════════════════════════╗")
        print("║                       Proceso interrumpido por el usuario              ║")
        print("╚══════════════════════════════════════════════════════════════════════╝\n")
        sys.exit(0)
    except Exception as e:
        print("\n\n╔══════════════════════════════════════════════════════════════════════╗")
        print("║                          ✗ ERROR INESPERADO                           ║")
        print("╚══════════════════════════════════════════════════════════════════════╝\n")
        print(f"Error: {e}\n")
        print("Stack trace:")
        import traceback
        traceback.print_exc()
        sys.exit(1)