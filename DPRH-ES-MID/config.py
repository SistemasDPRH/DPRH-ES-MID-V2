"""
Archivo de configuración global del sistema DPRH.
Permite centralizar parámetros sin modificar el código principal.
"""

# ==============================
# ARCHIVOS
# ==============================

INPUT_EXCEL = "input.xlsx"
OUTPUT_JSON = "empresas.dprh"
OUTPUT_PDF = "Estudio de Suelos y Prestaciones.pdf"

# ==============================
# VALIDACIÓN
# ==============================

OUTLIER_SUELDO_MAX = 1000000  # límite máximo permitido

# ==============================
# GRÁFICAS
# ==============================

GRAFICAS = {
    "empresas_sector": "empresas_sector.png",
    "histograma_sueldos": "histograma_sueldos.png",
    "prestaciones": "prestaciones.png"
}

# ==============================
# ESTILO PDF
# ==============================

PDF_TITLE = "ESTUDIO DE SUELDOS Y PRESTACIONES"
PDF_SUBTITLE = "Reporte generado automáticamente"

# ==============================
# REGLAS DE NEGOCIO
# ==============================

MIN_EMPRESAS_POR_PUESTO = 2

# ==============================
# OPCIONES
# ==============================

GENERAR_GRAFICAS = True
GENERAR_TEXTO_INTELIGENTE = True
APLICAR_VALIDACION = True
