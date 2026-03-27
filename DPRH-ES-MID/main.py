import json
from collections import defaultdict
import statistics

# ==============================
# CARGA DE DATOS
# ==============================

def cargar_datos(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

# ==============================
# FILTRAR PUESTOS VALIDOS
# ==============================

def obtener_puestos_validos(empresas):
    conteo = defaultdict(int)

    for empresa in empresas:
        puestos_unicos = set()
        for p in empresa['puestos']:
            puestos_unicos.add(p['nombre_puesto'])
        for puesto in puestos_unicos:
            conteo[puesto] += 1

    return {p for p, c in conteo.items() if c >= 2}

# ==============================
# AGRUPAR SUELDOS POR PUESTO
# ==============================

def agrupar_sueldos(empresas, puestos_validos):
    data = defaultdict(list)

    for empresa in empresas:
        for p in empresa['puestos']:
            if p['nombre_puesto'] in puestos_validos:
                data[p['nombre_puesto']].append({
                    'bruto': p['sueldo_bruto'],
                    'neto': p['sueldo_neto'],
                    'integrado': p['sueldo_integrado'],
                    'empleados': p['empleados_en_puesto']
                })
    return data

# ==============================
# CALCULOS ESTADISTICOS
# ==============================

def calcular_estadisticas(lista_valores):
    valores = sorted(lista_valores)
    return {
        'min': min(valores),
        'max': max(valores),
        'media': statistics.mean(valores),
        'mediana': statistics.median(valores),
        'q1': statistics.quantiles(valores, n=4)[0],
        'q3': statistics.quantiles(valores, n=4)[2],
        'std': statistics.stdev(valores) if len(valores) > 1 else 0
    }

# ==============================
# MEDIA PONDERADA
# ==============================

def media_ponderada(registros, key):
    total = sum(r[key] * r['empleados'] for r in registros)
    total_emp = sum(r['empleados'] for r in registros)
    return total / total_emp if total_emp > 0 else 0

# ==============================
# PROCESAR PUESTOS
# ==============================

def procesar_puestos(data):
    resultado = {}

    for puesto, registros in data.items():
        bruto = [r['bruto'] for r in registros]
        neto = [r['neto'] for r in registros]
        integrado = [r['integrado'] for r in registros]

        resultado[puesto] = {
            'bruto': calcular_estadisticas(bruto),
            'neto': calcular_estadisticas(neto),
            'integrado': calcular_estadisticas(integrado),
            'media_ponderada_bruto': media_ponderada(registros, 'bruto'),
            'media_ponderada_neto': media_ponderada(registros, 'neto'),
            'media_ponderada_integrado': media_ponderada(registros, 'integrado')
        }

    return resultado

# ==============================
# MAIN
# ==============================

def main():
    datos = cargar_datos('empresas.json')
    empresas = datos['empresas']

    puestos_validos = obtener_puestos_validos(empresas)
    sueldos = agrupar_sueldos(empresas, puestos_validos)
    resultado = procesar_puestos(sueldos)

    print("=== RESULTADO ===")
    for puesto, info in resultado.items():
        print(f"\nPuesto: {puesto}")
        print(info)

if __name__ == '__main__':
    main()
