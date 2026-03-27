"""
Genera texto dinámico para el reporte DPRH a partir de datos calculados.
Convierte números en insights tipo consultoría.
"""

# ==============================
# EMPRESAS
# ==============================

def resumen_empresas(empresas):
    total = len(empresas)
    total_empleados = sum(e['numero_empleados'] for e in empresas)
    promedio = total_empleados / total if total > 0 else 0

    return (
        f"El estudio se realizó con la participación de {total} empresas, "
        f"con un total de {total_empleados} empleados. "
        f"El promedio de empleados por empresa es de {round(promedio,2)}."
    )

# ==============================
# SECTOR
# ==============================

def analisis_sector(empresas):
    sectores = {}

    for e in empresas:
        s = e['sector']
        sectores[s] = sectores.get(s, 0) + 1

    total = len(empresas)

    frases = []
    for s, count in sectores.items():
        porcentaje = (count / total) * 100
        frases.append(f"{round(porcentaje,1)}% pertenecen al sector {s}")

    return "La distribución sectorial muestra que " + ", ".join(frases) + "."

# ==============================
# PRESTACIONES
# ==============================

def analisis_prestaciones(empresas):
    total = len(empresas)
    conteo_seguro = sum(1 for e in empresas if e['prestaciones']['seguro_vida'])

    porcentaje = (conteo_seguro / total) * 100 if total > 0 else 0

    return (
        f"El {round(porcentaje,1)}% de las empresas otorgan seguro de vida "
        f"como prestación a sus empleados."
    )

# ==============================
# SUELDOS POR PUESTO
# ==============================

def analisis_puesto(puesto, info):
    media = info['bruto']['media']
    minimo = info['bruto']['min']
    maximo = info['bruto']['max']

    return (
        f"Para el puesto {puesto}, el sueldo promedio es de {round(media,2)}, "
        f"con un rango que va desde {round(minimo,2)} hasta {round(maximo,2)}."
    )

# ==============================
# GENERADOR GENERAL
# ==============================

def generar_todos(empresas, resultado):
    textos = {}

    textos['empresas'] = resumen_empresas(empresas)
    textos['sector'] = analisis_sector(empresas)
    textos['prestaciones'] = analisis_prestaciones(empresas)

    textos['puestos'] = {
        puesto: analisis_puesto(puesto, info)
        for puesto, info in resultado.items()
    }