"""
Valida y limpia los datos antes de procesarlos.
Se usa después del excel_parser para evitar errores en cálculos.
"""

# ==============================
# VALIDACIONES GENERALES
# ==============================

def validar_empresas(empresas):
    empresas_validas = []

    for e in empresas:
        if not e.get('nombre'):
            continue

        if e.get('numero_empleados', 0) <= 0:
            continue

        empresas_validas.append(e)

    return empresas_validas

# ==============================
# VALIDAR PUESTOS
# ==============================

def validar_puestos(empresas):
    for e in empresas:
        puestos_validos = []

        for p in e.get('puestos', []):
            if not p.get('nombre_puesto'):
                continue

            if p.get('sueldo_bruto', 0) <= 0:
                continue

            puestos_validos.append(p)

        e['puestos'] = puestos_validos

    return empresas

# ==============================
# LIMPIAR OUTLIERS (OPCIONAL)
# ==============================

def limpiar_outliers(empresas, limite=1000000):
    for e in empresas:
        for p in e.get('puestos', []):
            if p['sueldo_bruto'] > limite:
                p['sueldo_bruto'] = limite

    return empresas

# ==============================
# PIPELINE DE VALIDACIÓN
# ==============================

def validar_todo(empresas):
    empresas = validar_empresas(empresas)
    empresas = validar_puestos(empresas)
    empresas = limpiar_outliers(empresas)

    return empresas
