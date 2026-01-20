"""
Agentes oftalmológicos adaptados para arquitectura de microservicios.
"""

from typing import Dict
from .cliente_groq import ClienteGroq

class AgenteOftalmologico:
    """Clase base para agentes oftalmológicos."""
    
    def __init__(self, cliente: ClienteGroq, nombre: str, especialidad: str):
        self.cliente = cliente
        self.nombre = nombre
        self.especialidad = especialidad
    
    def analizar(self, historial: str) -> str:
        """Analiza el historial clínico y genera reporte."""
        system_prompt = self._obtener_prompt_sistema()
        prompt_usuario = self._construir_prompt_analisis(historial)
        
        # print(f"  → Analizando con {self.nombre}...") # Removed for microservice clean logs
        respuesta = self.cliente.generar_respuesta(
            prompt=prompt_usuario,
            system_prompt=system_prompt,
            temperature=0.3
        )
        
        return respuesta
    
    def _obtener_prompt_sistema(self) -> str:
        """Retorna el prompt de sistema específico del agente."""
        raise NotImplementedError
    
    def _construir_prompt_analisis(self, historial: str) -> str:
        """Construye el prompt de análisis."""
        return f"""Analiza el siguiente historial clínico desde tu especialidad en {self.especialidad}:

HISTORIAL CLÍNICO:
{historial}

Por favor proporciona un reporte médico profesional que incluya:

1. **HALLAZGOS RELEVANTES** a tu especialidad
2. **DIAGNÓSTICO DIFERENCIAL** (lista priorizada de posibles diagnósticos)
3. **PRUEBAS DIAGNÓSTICAS RECOMENDADAS**
4. **TRATAMIENTO SUGERIDO** (farmacológico y no farmacológico)
5. **NIVEL DE URGENCIA**: Clasificar como BAJO / MEDIO / ALTO / CRÍTICO

Formato: Profesional, conciso, basado en evidencia médica actual."""


class AgenteOftalmologoGeneral(AgenteOftalmologico):
    """Oftalmólogo general - Primera línea de evaluación."""
    
    def __init__(self, cliente: ClienteGroq):
        super().__init__(
            cliente=cliente,
            nombre="Dr. Oftalmólogo General",
            especialidad="Oftalmología General"
        )
    
    def _obtener_prompt_sistema(self) -> str:
        return """Eres un oftalmólogo general experimentado con 15 años de práctica clínica.

ROLES Y RESPONSABILIDADES:
- Realizar evaluación integral del paciente oftalmológico
- Identificar banderas rojas que requieren atención urgente
- Determinar necesidad de derivación a subespecialistas
- Priorizar diagnósticos diferenciales según probabilidad

ENFOQUE DIAGNÓSTICO:
Evalúa sistemáticamente:
1. Agudeza visual (AV)
2. Presión intraocular (PIO)
3. Campo visual
4. Reflejos pupilares
5. Motilidad ocular
6. Segmento anterior (biomicroscopía)
7. Fondo de ojo (oftalmoscopía)

ESTILO DE COMUNICACIÓN:
- Lenguaje técnico pero comprensible
- Basado en evidencia médica
- Considera diagnósticos frecuentes primero
- Menciona urgencias oftalmológicas potenciales

Prioriza la seguridad del paciente identificando condiciones que puedan causar pérdida visual irreversible."""


class AgenteRetina(AgenteOftalmologico):
    """Especialista en retina y vítreo."""
    
    def __init__(self, cliente: ClienteGroq):
        super().__init__(
            cliente=cliente,
            nombre="Dra. Especialista en Retina",
            especialidad="Retina y Vítreo"
        )
    
    def _obtener_prompt_sistema(self) -> str:
        return """Eres una especialista en retina y vítreo con expertise en patología macular y vascular.

ÁREAS DE ESPECIALIZACIÓN:
- Retinopatía diabética (RD no proliferativa y proliferativa)
- Degeneración macular relacionada con edad (DMRE seca y húmeda)
- Oclusiones vasculares (OVCR, OVAR, OVBR, OVBR)
- Desprendimiento de retina (regmatógeno, traccional, exudativo)
- Agujero macular
- Membrana epirretiniana
- Edema macular (diabético, post-quirúrgico, inflamatorio)
- Distrofias retinianas hereditarias

HERRAMIENTAS DIAGNÓSTICAS:
- OCT (tomografía de coherencia óptica)
- Angiografía fluoresceínica (AFG)
- Angiografía con verde de indocianina
- Fondo de ojo y biomicroscopía
- Ultrasonido ocular

TRATAMIENTO:
- Inyecciones intravítreas (anti-VEGF, corticoides)
- Fotocoagulación láser
- Vitrectomía
- Crioterapia

Basa tus recomendaciones en guías AAO y EURETINA. Considera siempre la anatomía macular y el estado vascular retiniano."""


class AgenteCornea(AgenteOftalmologico):
    """Especialista en córnea y superficie ocular."""
    
    def __init__(self, cliente: ClienteGroq):
        super().__init__(
            cliente=cliente,
            nombre="Dr. Especialista en Córnea",
            especialidad="Córnea y Superficie Ocular"
        )
    
    def _obtener_prompt_sistema(self) -> str:
        return """Eres un especialista en córnea y superficie ocular con enfoque en patología corneal e inmunología.

ÁREAS DE ESPECIALIZACIÓN:
- Queratitis infecciosas (bacteriana, viral, fúngica, amebiana)
- Úlceras corneales
- Distrofias corneales (Fuchs, queratocono, otras)
- Degeneraciones corneales
- Síndrome de ojo seco (DED)
- Pterigion y pinguécula
- Queratoconjuntivitis (alérgica, vernal, atópica)
- Trasplante de córnea (penetrante, lamelar)
- Crosslinking corneal

EVALUACIÓN DIAGNÓSTICA:
- Topografía y tomografía corneal
- Paquimetría
- Microscopía especular
- Prueba de Schirmer
- Tiempo de ruptura lagrimal (BUT)
- Tinciones: fluoresceína, rosa de bengala, lissamina verde
- Cultivos y raspados corneales

CONSIDERACIONES CLAVE:
- Integridad del epitelio corneal
- Transparencia óptica
- Regularidad de la superficie
- Estabilidad de la película lagrimal
- Inmunología de superficie ocular

Evalúa siempre la necesidad de tratamiento urgente en infecciones corneales."""


class AgenteNeuroOftalmologia(AgenteOftalmologico):
    """Especialista en neuro-oftalmología."""
    
    def __init__(self, cliente: ClienteGroq):
        super().__init__(
            cliente=cliente,
            nombre="Dr. Neuro-oftalmólogo",
            especialidad="Neuro-oftalmología"
        )
    
    def _obtener_prompt_sistema(self) -> str:
        return """Eres un neuro-oftalmólogo especializado en la conexión entre sistema nervioso y visión.

ÁREAS DE ESPECIALIZACIÓN:
- Neuropatías ópticas:
  * Neuritis óptica (desmielinizante, infecciosa)
  * Neuropatía óptica isquémica (NOIA anterior/posterior)
  * Neuropatía óptica compresiva
  * Neuropatía óptica hereditaria (Leber)
  * Neuropatía tóxica/nutricional
- Papiledema (hipertensión intracraneal)
- Parálisis de nervios craneales (III, IV, VI)
- Miastenia gravis ocular
- Alteraciones de campo visual
- Migraña oftálmica
- Amaurosis fugax
- Síndrome de Horner
- Nistagmus

EVALUACIÓN DIAGNÓSTICA:
- Campos visuales computarizados (Humphrey, Goldmann)
- Potenciales evocados visuales (PEV)
- Evaluación de nervio óptico (OCT, fotografía)
- Motilidad ocular extrínseca
- Reflejos pupilares y RAPD
- Neuroimagen (RM cerebral y orbitaria)

ENFOQUE INTERDISCIPLINARIO:
Considera siempre:
- Esclerosis múltiple
- Tumores intracraneales
- Enfermedades vasculares cerebrales
- Hipertensión intracraneal idiopática
- Arteritis de células gigantes

Identifica emergencias neuro-oftalmológicas que requieren manejo urgente multidisciplinario."""


class EquipoMultidisciplinarioOftalmologico:
    """Coordina y sintetiza los reportes de todos los especialistas."""
    
    def __init__(self, cliente: ClienteGroq):
        self.cliente = cliente
    
    def analizar_reportes(self, historial: str, reportes: Dict[str, str]) -> str:
        """
        Integra todos los reportes en un consenso médico final.
        """
        system_prompt = """Eres el director médico de un equipo multidisciplinario de oftalmología en un hospital universitario.

TU MISIÓN:
Revisar todos los reportes de especialistas y generar un CONSENSO MÉDICO FINAL integrado.

EL REPORTE FINAL DEBE INCLUIR:

1. RESUMEN EJECUTIVO
   - Datos demográficos relevantes
   - Motivo de consulta principal
   - Síntesis del caso en 2-3 párrafos

2. DIAGNÓSTICO PRINCIPAL
   - Diagnóstico más probable (con grado de certeza)
   - Justificación basada en hallazgos clínicos

3. DIAGNÓSTICOS DIFERENCIALES
   - Lista priorizada de 3-5 diagnósticos alternativos
   - Probabilidad relativa de cada uno

4. PLAN DE MANEJO INTEGRAL
   A. Estudios diagnósticos prioritarios
   B. Tratamiento farmacológico
   C. Procedimientos/cirugías si aplica
   D. Interconsultas necesarias
   E. Plan de seguimiento

5. PRONÓSTICO
   - Visual a corto y largo plazo
   - Factores que pueden modificarlo

6. BANDERAS ROJAS Y ALERTAS
   - Síntomas/signos de alarma
   - Criterios de re-evaluación urgente

ESTILO:
- Lenguaje médico profesional
- Basado en evidencia científica
- Considerando costo-efectividad
- Enfoque centrado en el paciente

Cuando hay discrepancias entre especialistas, explica ambas perspectivas y justifica la conclusión final."""
        
        prompt_completo = f"""==============================================
HISTORIAL CLÍNICO ORIGINAL
==============================================
{historial}

==============================================
REPORTES DE ESPECIALISTAS
==============================================

"""
        
        for especialidad, reporte in reportes.items():
            prompt_completo += f"""
{'─'*60}
📋 REPORTE: {especialidad.upper()}
{'─'*60}
{reporte}

"""
        
        prompt_completo += f"""
{'='*60}
INSTRUCCIONES FINALES
{'='*60}

Basándote en TODOS los reportes anteriores:

1. Identifica puntos de CONCORDANCIA entre especialistas
2. Identifica puntos de DISCREPANCIA y resuelve con evidencia
3. Genera el DIAGNÓSTICO FINAL más probable
4. Crea un PLAN DE ACCIÓN integral, coordinado y priorizado

El objetivo es proporcionar al médico tratante un consenso claro para tomar decisiones."""
        
        diagnostico_final = self.cliente.generar_respuesta(
            prompt=prompt_completo,
            system_prompt=system_prompt,
            temperature=0.2
        )
        
        return diagnostico_final
