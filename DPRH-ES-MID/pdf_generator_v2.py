from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import json

from charts import generar_todas

"""
Versión mejorada del generador de PDF.
Incluye gráficas y mejor estructura visual.
"""

OUTPUT_PDF = "reporte_dprh_v2.pdf"
styles = getSampleStyleSheet()

# ==============================
# UTILIDADES
# ==============================

def cargar_datos(path="empresas.json"):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def titulo(texto):
    return Paragraph(f"<b>{texto}</b>", styles['Heading2'])


def subtitulo(texto):
    return Paragraph(f"<b>{texto}</b>", styles['Heading3'])


def parrafo(texto):
    return Paragraph(texto, styles['Normal'])


def tabla(data):
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black)
    ]))
    return t

# ==============================
# SECCIONES
# ==============================

def portada(story):
    story.append(Spacer(1, 50))
    story.append(Paragraph("<b>ESTUDIO DE SUELDOS Y PRESTACIONES</b>", styles['Title']))
    story.append(Spacer(1, 20))
    story.append(parrafo("Reporte generado automáticamente"))
    story.append(Spacer(1, 40))


def seccion_empresas(story, empresas):
    story.append(titulo("Empresas Participantes"))
    story.append(Spacer(1, 10))

    data = [["Empresa", "Empleados"]]
    for e in empresas:
        data.append([e['nombre'], e['numero_empleados']])

    story.append(tabla(data))
    story.append(Spacer(1, 20))

    story.append(subtitulo("Distribución por sector"))
    story.append(Image("empresas_sector.png", width=400, height=300))
    story.append(Spacer(1, 20))


def seccion_sueldos(story, resultado):
    story.append(titulo("Evaluación de Puestos"))
    story.append(Spacer(1, 10))

    for puesto, info in resultado.items():
        story.append(subtitulo(puesto))

        data = [
            ["Tipo", "Min", "Max", "Media", "Mediana"],
            ["Bruto", info['bruto']['min'], info['bruto']['max'], info['bruto']['media'], info['bruto']['mediana']],
            ["Neto", info['neto']['min'], info['neto']['max'], info['neto']['media'], info['neto']['mediana']],
            ["Integrado", info['integrado']['min'], info['integrado']['max'], info['integrado']['media'], info['integrado']['mediana']]
        ]

        story.append(tabla(data))
        story.append(Spacer(1, 10))

    story.append(subtitulo("Distribución salarial"))
    story.append(Image("histograma_sueldos.png", width=400, height=300))
    story.append(Spacer(1, 20))


def seccion_prestaciones(story):
    story.append(titulo("Prestaciones"))
    story.append(Spacer(1, 10))
    story.append(Image("prestaciones.png", width=400, height=300))
    story.append(Spacer(1, 20))

# ==============================
# GENERAR PDF
# ==============================

def generar_pdf(empresas, resultado):
    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=letter)
    story = []

    portada(story)
    seccion_empresas(story, empresas)
    seccion_sueldos(story, resultado)
    seccion_prestaciones(story)

    doc.build(story)

# ==============================
# MAIN
# ==============================

def main():
    datos = cargar_datos()
    empresas = datos['empresas']

    from main import obtener_puestos_validos, agrupar_sueldos, procesar_puestos

    puestos_validos = obtener_puestos_validos(empresas)
    sueldos = agrupar_sueldos(empresas, puestos_validos)
    resultado = procesar_puestos(sueldos)

    # Generar gráficas antes del PDF
    generar_todas(empresas, sueldos)

    generar_pdf(empresas, resultado)
    print(f"PDF generado: {OUTPUT_PDF}")


if __name__ == '__main__':
    main()
