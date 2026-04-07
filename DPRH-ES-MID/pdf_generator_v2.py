from reportlab.platypus import *
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt

# =============================
# CONFIG
# =============================

LOGO_PATH = "assets/logo.png"
GRAFICA1 = "grafica_sueldos.png"
GRAFICA2 = "grafica_promedios.png"

COLOR_PRIMARIO = colors.HexColor("#1F3A5F")
COLOR_SECUNDARIO = colors.HexColor("#EAECEE")

# =============================
# ESTILOS
# =============================

styles = getSampleStyleSheet()

titulo = ParagraphStyle(name="titulo", fontSize=18, textColor=COLOR_PRIMARIO, spaceAfter=10)
kpi = ParagraphStyle(name="kpi", fontSize=16, alignment=1, fontName="Helvetica-Bold")
kpi_label = ParagraphStyle(name="kpi_label", fontSize=9, alignment=1, textColor=colors.grey)
texto = ParagraphStyle(name="texto", fontSize=10)

# =============================
# HEADER / FOOTER
# =============================

def header_footer(canvas, doc):
    canvas.saveState()

    if os.path.exists(LOGO_PATH):
        canvas.drawImage(LOGO_PATH, 40, 735, width=60, height=30)

    canvas.setFont("Helvetica", 9)
    canvas.drawString(110, 750, "Dashboard Salarial - Mérida 2025")

    canvas.setFillColor(colors.grey)
    canvas.drawString(40, 30, datetime.now().strftime("%d/%m/%Y"))
    canvas.drawRightString(550, 30, f"Página {doc.page}")

    canvas.restoreState()

# =============================
# DATA
# =============================

def cargar_empresas():
    try:
        with open("empresas.json", "r", encoding="utf-8") as f:
            return json.load(f).get("empresas", [])
    except:
        return []

# =============================
# KPIs
# =============================

def calcular_kpis(empresas):
    total_empresas = len(empresas)
    total_puestos = 0
    sueldos = []

    for e in empresas:
        for p in e.get("puestos", []):
            total_puestos += 1
            sueldos.append(p.get("sueldo_bruto", 0))

    promedio = sum(sueldos)/len(sueldos) if sueldos else 0
    maximo = max(sueldos) if sueldos else 0

    return total_empresas, total_puestos, promedio, maximo

def bloque_kpi(valor, label):
    return Table([
        [Paragraph(f"{valor}", kpi)],
        [Paragraph(label, kpi_label)]
    ], colWidths=120, rowHeights=[30,20],
    style=[("BOX",(0,0),(-1,-1),1,colors.grey)])

# =============================
# GRAFICAS
# =============================

def grafica_sueldos(empresas):
    puestos = []
    sueldos = []

    for e in empresas:
        for p in e.get("puestos", [])[:5]:
            puestos.append(p.get("nombre_puesto",""))
            sueldos.append(p.get("sueldo_bruto",0))

    if not puestos:
        return

    plt.figure()
    plt.barh(puestos, sueldos)
    plt.title("Top Sueldos")
    plt.tight_layout()
    plt.savefig(GRAFICA1)
    plt.close()

def grafica_promedio(empresas):
    nombres = []
    promedios = []

    for e in empresas:
        sueldos = [p.get("sueldo_bruto",0) for p in e.get("puestos",[])]
        if sueldos:
            nombres.append(e.get("nombre",""))
            promedios.append(sum(sueldos)/len(sueldos))

    if not nombres:
        return

    plt.figure()
    plt.bar(nombres, promedios)
    plt.xticks(rotation=45)
    plt.title("Promedio por Empresa")
    plt.tight_layout()
    plt.savefig(GRAFICA2)
    plt.close()

# =============================
# RESUMEN IA
# =============================

def resumen_automatico(empresas):
    total, puestos, prom, maximo = calcular_kpis(empresas)

    return f"""
El análisis incluye {total} empresas con un total de {puestos} puestos evaluados.
El sueldo promedio es de ${prom:,.0f}, mientras que el sueldo más alto registrado es de ${maximo:,.0f}.
Se observan variaciones importantes entre empresas, lo cual refleja diferencias en estructura organizacional y competitividad salarial.
"""

# =============================
# TABLA
# =============================

def tabla(empresas):
    data = [["Puesto", "Bruto"]]

    for e in empresas:
        for p in e.get("puestos", []):
            data.append([
                p.get("nombre_puesto",""),
                f"${p.get('sueldo_bruto',0):,.0f}"
            ])

    t = Table(data, colWidths=[300,100])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),COLOR_PRIMARIO),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.25,colors.grey)
    ]))
    return t

# =============================
# PDF
# =============================

def generar_pdf():
    empresas = cargar_empresas()

    grafica_sueldos(empresas)
    grafica_promedio(empresas)

    doc = SimpleDocTemplate(
        "Estudio Dashboard DPRH.pdf",
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    story = []

    # Titulo
    story.append(Paragraph("DASHBOARD SALARIAL", titulo))

    # KPIs
    total, puestos, prom, maximo = calcular_kpis(empresas)

    kpis = Table([
        [
            bloque_kpi(total, "Empresas"),
            bloque_kpi(puestos, "Puestos"),
            bloque_kpi(f"${prom:,.0f}", "Promedio"),
            bloque_kpi(f"${maximo:,.0f}", "Máximo")
        ]
    ])
    story.append(kpis)
    story.append(Spacer(1,20))

    # Resumen
    story.append(Paragraph("RESUMEN EJECUTIVO", titulo))
    story.append(Paragraph(resumen_automatico(empresas), texto))

    story.append(Spacer(1,20))

    # Graficas
    if os.path.exists(GRAFICA1):
        story.append(Image(GRAFICA1, width=400, height=200))

    if os.path.exists(GRAFICA2):
        story.append(Image(GRAFICA2, width=400, height=200))

    story.append(Spacer(1,20))

    # Tabla
    story.append(Paragraph("DETALLE DE SUELDOS", titulo))
    story.append(tabla(empresas))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

    print("PDF estilo dashboard generado")

# =============================
# MAIN
# =============================

if __name__ == "__main__":
    generar_pdf()