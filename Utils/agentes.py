"""
Módulo: agentes.py
Descripción: Define los agentes especialistas oftalmológicos y sus prompts.
Idioma: Español
"""

from .cliente_gemini import ClienteGemini

class Agente:
    """Clase base para todos los agentes médicos."""
    
    def __init__(self, nombre: str, especialidad: str, cliente_gemini: ClienteGemini):
        self.nombre = nombre
        self.especialidad = especialidad
        self.cliente = cliente_gemini

    def analizar(self, historial_clinico: str) -> str:
        """Método genérico para realizar el análisis."""
        prompt = self._construir_prompt(historial_clinico)
        print(f"--- Agente {self.nombre} ({self.especialidad}) analizando... ---")
        respuesta = self.cliente.generar_respuesta(prompt)
        return respuesta

    def _construir_prompt(self, historial_clinico: str) -> str:
        """Debe ser implementado por las subclases."""
        raise NotImplementedError("Cada agente debe definir su propio prompt.")


class AgenteOftalmologoGeneral(Agente):
    def __init__(self, cliente_gemini: ClienteGemini):
        super().__init__("Dr. General", "Oftalmología General", cliente_gemini)

    def _construir_prompt(self, historial_clinico: str) -> str:
        return f"""
        ROL: Eres un Oftalmólogo General experto.
        TAREA: Analizar el siguiente historial clínico buscando problemas de agudeza visual, presión intraocular y síntomas sistémicos generales.
        
        HISTORIAL CLÍNICO:
        {historial_clinico}
        
        INSTRUCCIONES:
        1. Identifica la Agudeza Visual (AV) y determina si es anormal.
        2. Evalúa la Presión Intraocular (PIO) para descartar riesgo de glaucoma agudo.
        3. Identifica antecedentes sistémicos (Diabetes, Hipertensión) relevantes para el ojo.
        4. Resume los síntomas principales.
        
        FORMATO DE SALIDA (Solo texto plano, se conciso):
        - Hallazgos Principales: [Lista breve]
        - Signos de Alerta: [Si/No y por qué]
        - Recomendación Inicial: [Tu sugerencia breve]
        """


class AgenteRetina(Agente):
    def __init__(self, cliente_gemini: ClienteGemini):
        super().__init__("Dra. Retina", "Retina y Vítreo", cliente_gemini)

    def _construir_prompt(self, historial_clinico: str) -> str:
        return f"""
        ROL: Eres un especialista en Retina y Vítreo.
        TAREA: Analizar el historial clínico buscando patologías de fondo de ojo, mácula y vítreo.
        
        HISTORIAL CLÍNICO:
        {historial_clinico}
        
        INSTRUCCIONES:
        1. Busca signos de Retinopatía Diabética (hemorragias, exudados, neovasos).
        2. Evalúa el estado de la mácula (edema, agujeros, membranas).
        3. Analiza el vítreo (hemorragias, desprendimiento).
        4. Evalúa riesgo de Desprendimiento de Retina.
        
        FORMATO DE SALIDA (Se muy técnico y preciso):
        - Análisis de Fondo de Ojo: [Detalle]
        - Patología Retiniana Detectada: [Nombre de la patología sospechada]
        - Gravedad: [Leve/Moderada/Severa]
        - Tratamiento Sugerido: [Láser/Inyección/Cirugía/Observación]
        """


class AgenteCornea(Agente):
    def __init__(self, cliente_gemini: ClienteGemini):
        super().__init__("Dr. Córnea", "Córnea y Superficie Ocular", cliente_gemini)

    def _construir_prompt(self, historial_clinico: str) -> str:
        return f"""
        ROL: Eres un especialista en Córnea y Superficie Ocular.
        TAREA: Analizar exclusivamente la superficie ocular, córnea y cámara anterior.
        
        HISTORIAL CLÍNICO:
        {historial_clinico}
        
        INSTRUCCIONES:
        1. Evalúa la transparencia de la córnea.
        2. Revisa la cámara anterior (profundidad, células).
        3. Descarta infecciones, queratocono o síndrome de ojo seco severo.
        4. Si no hay datos relevantes de tu área, indícalo claramente.
        
        FORMATO DE SALIDA:
        - Estado Corneal: [Normal/Anormal]
        - Hallazgos Superficie Ocular: [Detalle]
        - Conclusión: [Tu opinión desde tu subespecialidad]
        """


class AgenteNeuroOftalmologia(Agente):
    def __init__(self, cliente_gemini: ClienteGemini):
        super().__init__("Dra. Neuro", "Neuro-Oftalmología", cliente_gemini)

    def _construir_prompt(self, historial_clinico: str) -> str:
        return f"""
        ROL: Eres especialista en Neuro-Oftalmología.
        TAREA: Analizar nervio óptico, pupila y campos visuales.
        
        HISTORIAL CLÍNICO:
        {historial_clinico}
        
        INSTRUCCIONES:
        1. Analiza la excavación y color del nervio óptico.
        2. Interpreta los campos visuales si están reportados.
        3. Relaciona síntomas neurológicos (migrañas, visión doble) si existen.
        4. Diferencia entre problema ocular vs problema neurológico.
        
        FORMATO DE SALIDA:
        - Evaluación Nervio Óptico: [Detalle]
        - Interpretación Campos Visuales: [Detalle]
        - Diagnóstico Neurológico Probable: [Si aplica]
        """


class EquipoMultidisciplinarioOftalmologico(Agente):
    def __init__(self, cliente_gemini: ClienteGemini):
        super().__init__("Director Médico", "Integración Diagnóstica", cliente_gemini)

    def analizar_reportes(self, historial_original: str, reportes_agentes: dict) -> str:
        """
        Método especializado que recibe los reportes de los otros agentes y genera el diagnóstico final.
        """
        texto_reportes = ""
        for especialista, reporte in reportes_agentes.items():
            texto_reportes += f"\n--- REPORTE {especialista.upper()} ---\n{reporte}\n"

        prompt = f"""
        ROL: Eres el Director Médico de una clínica oftalmológica de alto nivel.
        TAREA: Integrar los reportes de tus especialistas y generar un Diagnóstico Final Definitivo y Profesional.
        
        CONTEXTO DEL PACIENTE:
        {historial_original}
        
        REPORTES DE LOS ESPECIALISTAS:
        {texto_reportes}
        
        INSTRUCCIONES:
        1. Lee todos los reportes y busca el consenso.
        2. Si hay contradicciones, decide basándote en la evidencia clínica más fuerte del historial.
        3. Prioriza las patologías que amenazan la visión.
        4. Genera 3 posibles diagnósticos en orden de probabilidad.
        
        FORMATO DE SALIDA (Formato Markdown Médico Profesional):
        
        # INFORME DE DIAGNÓSTICO INTEGRAL OFTALMOLÓGICO
        
        ## 1. RESUMEN DEL CASO
        [Resumen breve de 2-3 líneas]
        
        ## 2. ANÁLISIS DE ESPECIALIDADES
        - **Oftalmología General**: [Resumen hallazgo clave]
        - **Retina**: [Resumen hallazgo clave]
        - **Córnea**: [Resumen hallazgo clave]
        - **Neuro-Oftalmología**: [Resumen hallazgo clave]
        
        ## 3. DIAGNÓSTICOS DIFERENCIALES (Probabilidad)
        1. **[DIAGNÓSTICO PRINCIPAL]** (Alta probabilidad):
           - *Justificación*: ...
           - *Plan de Acción*: ...
           
        2. **[Diagnóstico secundario]** (Media probabilidad):
           - *Justificación*: ...
        
        3. **[Diagnóstico terciario]** (Baja probabilidad):
           - *Justificación*: ...
           
        ## 4. CONCLUSIÓN Y RECOMENDACIÓN FINAL
        [Párrafo final de cierre profesional]
        
        Firma:
        Sistema de Agentes de IA Oftalmológica
        """
        
        print(f"--- {self.nombre} generando consenso final... ---")
        return self.cliente.generar_respuesta(prompt)

    def _construir_prompt(self, historial_clinico: str) -> str:
        return "" # No se usa directamente, usa analizar_reportes
