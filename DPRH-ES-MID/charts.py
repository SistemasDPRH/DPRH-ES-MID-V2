import matplotlib.pyplot as plt
from collections import Counter

"""
Módulo para generar gráficas del estudio DPRH.
Guarda imágenes que luego pueden insertarse en el PDF.
"""

# ==============================
# GRAFICA 1: EMPRESAS POR SECTOR
# ==============================

def grafica_empresas_por_sector(empresas, output="empresas_sector.png"):
    sectores = [e['sector'] for e in empresas]
    conteo = Counter(sectores)

    labels = list(conteo.keys())
    valores = list(conteo.values())

    plt.figure()
    plt.pie(valores, labels=labels, autopct='%1.1f%%')
    plt.title("Distribución de Empresas por Sector")
    plt.savefig(output)
    plt.close()

# ==============================
# GRAFICA 2: DISTRIBUCION SALARIAL
# ==============================

def grafica_histograma_sueldos(data, output="histograma_sueldos.png"):
    sueldos = []

    for puesto, registros in data.items():
        for r in registros:
            sueldos.append(r['bruto'])

    plt.figure()
    plt.hist(sueldos, bins=20)
    plt.title("Distribución Salarial (Bruto)")
    plt.xlabel("Sueldo")
    plt.ylabel("Frecuencia")
    plt.savefig(output)
    plt.close()

# ==============================
# GRAFICA 3: PRESTACIONES
# ==============================

def grafica_prestaciones(empresas, output="prestaciones.png"):
    prestaciones_keys = [
        'seguro_vida', 'seguro_gastos_medicos', 'fondo_ahorro',
        'bonos', 'utilidades', 'comedor', 'transporte', 'vales'
    ]

    conteo = {k: 0 for k in prestaciones_keys}

    for e in empresas:
        for k in prestaciones_keys:
            if e['prestaciones'].get(k):
                conteo[k] += 1

    labels = list(conteo.keys())
    valores = list(conteo.values())

    plt.figure()
    plt.bar(labels, valores)
    plt.title("Prestaciones otorgadas")
    plt.xticks(rotation=45)
    plt.savefig(output)
    plt.close()

# ==============================
# GENERAR TODAS
# ==============================

def generar_todas(empresas, sueldos_data):
    grafica_empresas_por_sector(empresas)
    grafica_histograma_sueldos(sueldos_data)
    grafica_prestaciones(empresas)

    print("Gráficas generadas correctamente")
