from reportlab.platypus import PageTemplate, Frame
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

"""
Este módulo controla el diseño del PDF:
- Márgenes
- Encabezados
- Pies de página
- Numeración
"""

# ==============================
# ENCABEZADO
# ==============================

def draw_header(canvas: canvas.Canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(inch, 10.5 * inch, "Estudio de Sueldos y Prestaciones")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(7.5 * inch, 10.5 * inch, f"Página {doc.page}")
    canvas.restoreState()

# ==============================
# PIE DE PÁGINA
# ==============================

def draw_footer(canvas: canvas.Canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(inch, 0.5 * inch, "Confidencial - Uso exclusivo")
    canvas.restoreState()

# ==============================
# PLANTILLA DE PÁGINA
# ==============================

def get_page_template():
    frame = Frame(
        inch,
        inch,
        6.5 * inch,
        9 * inch,
        id='normal'
    )

    template = PageTemplate(
        id='template_dprh',
        frames=[frame],
        onPage=draw_header,
        onPageEnd=draw_footer
    )

    return template

# ==============================
# APLICAR A DOCUMENTO
# ==============================

def aplicar_layout(doc):
    template = get_page_template()
    doc.addPageTemplates([template])
