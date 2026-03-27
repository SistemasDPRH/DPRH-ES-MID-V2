from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import json

"""
Genera el PDF final a partir del resultado procesado.
Depende de main.py (o datos ya calculados en JSON).
"""

OUTPUT_PDF = "reporte_dprh.pdf"

styles = getSampleStyleSheet()

# ==============================
# UTILIDADES
# ==============================

def cargar_datos(path="empresas.json"):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def titulo(texto):
    return Paragraph(f"<b>{texto}</b>", styles['Heading2'])


def parrafo(texto):
    return Paragraph(texto, styles['Normal'])


def tabla(data):
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    return t

# ==============================
# SECCIONES
# ==============================

def seccion_responsabilidad(story):
    story.append(titulo("I. Nuestra Responsabilidad"))
    story.append(Spacer(1, 10))
    story.append(parrafo("Este estudio es confidencial y de uso exclusivo del cliente."))
    story.append(Spacer(1, 20))


def seccion_objetivo(story):
    story.append(titulo("II. Objetivo"))
    story.append(Spacer(1, 10))
    story.append(parrafo("Analizar comparativamente sueldos y prestaciones."))
    story.append(Spacer(1, 20))


def seccion_empresas(story, empresas):
    story.append(titulo("III. Empresas Participantes"))
    story.append(Spacer(1, 10))

    data = [["Empresa", "Empleados"]]
    for e in empresas:
        data.append([e['nombre'], e['numero_empleados']])

    story.append(tabla(data))
    story.append(Spacer(1, 20))


def seccion_puestos(story, resultado):
    story.append(titulo("IV. Evaluación de Puestos"))
    story.append(Spacer(1, 10))

    for puesto, info in resultado.items():
        story.append(parrafo(f"<b>{puesto}</b>"))

        data = [
            ["Tipo", "Min", "Max", "Media", "Mediana"],
            ["Bruto", info['bruto']['min'], info['bruto']['max'], info['bruto']['media'], info['bruto']['mediana']],
            ["Neto", info['neto']['min'], info['neto']['max'], info['neto']['media'], info['neto']['mediana']],
            ["Integrado", info['integrado']['min'], info['integrado']['max'], info['integrado']['media'], info['integrado']['mediana']]
        ]

        story.append(tabla(data))
        story.append(Spacer(1, 15))

# ==============================
# GENERAR PDF
# ==============================

def generar_pdf(empresas, resultado):
    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=letter)
    story = []

    seccion_responsabilidad(story)
    seccion_objetivo(story)
    seccion_empresas(story, empresas)
    seccion_puestos(story, resultado)

    doc.build(story)

# ==============================
# MAIN
# ==============================

def main():
    datos = cargar_datos()
    empresas = datos['empresas']

    # Importar cálculo desde main (simplificado)
    from main import obtener_puestos_validos, agrupar_sueldos, procesar_puestos

    puestos_validos = obtener_puestos_validos(empresas)
    sueldos = agrupar_sueldos(empresas, puestos_validos)
    resultado = procesar_puestos(sueldos)

    generar_pdf(empresas, resultado)
    print(f"PDF generado: {OUTPUT_PDF}")


if __name__ == '__main__':
    main()
