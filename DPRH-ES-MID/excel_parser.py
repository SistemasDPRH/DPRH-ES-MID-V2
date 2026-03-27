import pandas as pd
import json
from collections import defaultdict

"""
Este script lee un archivo Excel con información de múltiples empresas y lo
transforma a la estructura requerida por main.py (empresas.json).

Suposiciones del Excel (puedes ajustar los nombres de columnas abajo):
- Una sola hoja con todas las empresas (o especifica sheet_name)
- Columnas esperadas:
    Empresa, Sector, Puesto, Area, EmpleadosPuesto,
    SueldoBruto, SueldoNeto, SueldoIntegrado,
    NumEmpleadosEmpresa, Sindicalizados, NoSindicalizados,
    Aguinaldo, PrimaVacacional, DiasVacaciones,
    SeguroVida, SeguroGastosMedicos, FondoAhorro,
    Bonos, Utilidades, Comedor, Transporte, Vales, PrevisionSocial,
    RotacionAnual, Rotacion30, Rotacion90, Rotacion180,
    TieneContrato, Sindicato, AumentoSalarial

Puedes mapear/renombrar columnas en el diccionario COLUMN_MAP.
"""

# ==============================
# CONFIGURACIÓN
# ==============================

EXCEL_PATH = "input.xlsx"
OUTPUT_JSON = "empresas.json"
SHEET_NAME = 0  # o nombre de hoja

# Mapeo de columnas del Excel a claves internas
COLUMN_MAP = {
    "Empresa": "empresa",
    "Sector": "sector",
    "Puesto": "puesto",
    "Area": "area",
    "EmpleadosPuesto": "empleados_puesto",
    "SueldoBruto": "bruto",
    "SueldoNeto": "neto",
    "SueldoIntegrado": "integrado",
    "NumEmpleadosEmpresa": "num_emp",
    "Sindicalizados": "sind",
    "NoSindicalizados": "nosind",
    "Aguinaldo": "aguinaldo",
    "PrimaVacacional": "prima",
    "DiasVacaciones": "vacaciones",
    "SeguroVida": "seg_vida",
    "SeguroGastosMedicos": "sgmm",
    "FondoAhorro": "fondo",
    "Bonos": "bonos",
    "Utilidades": "util",
    "Comedor": "comedor",
    "Transporte": "transporte",
    "Vales": "vales",
    "PrevisionSocial": "prev",
    "RotacionAnual": "rot_anual",
    "Rotacion30": "rot30",
    "Rotacion90": "rot90",
    "Rotacion180": "rot180",
    "TieneContrato": "contrato",
    "Sindicato": "sindicato",
    "AumentoSalarial": "aumento"
}

# ==============================
# UTILIDADES
# ==============================

def to_bool(val):
    if pd.isna(val):
        return False
    if isinstance(val, bool):
        return val
    val = str(val).strip().lower()
    return val in ["1", "true", "si", "sí", "yes", "x"]


def to_float(val):
    if pd.isna(val):
        return 0.0
    try:
        return float(val)
    except Exception:
        # limpiar posibles símbolos
        s = str(val).replace(",", "").replace("$", "").strip()
        try:
            return float(s)
        except Exception:
            return 0.0


def to_int(val):
    if pd.isna(val):
        return 0
    try:
        return int(float(val))
    except Exception:
        return 0

# ==============================
# LECTURA Y NORMALIZACIÓN
# ==============================

def leer_excel(path=EXCEL_PATH, sheet=SHEET_NAME):
    df = pd.read_excel(path, sheet_name=sheet)

    # Normalizar nombres de columnas
    df.columns = [c.strip() for c in df.columns]

    # Validar columnas mínimas
    faltantes = [c for c in COLUMN_MAP.keys() if c not in df.columns]
    if faltantes:
        print("[WARN] Faltan columnas en el Excel:", faltantes)

    return df

# ==============================
# TRANSFORMACIÓN A ESTRUCTURA
# ==============================

def construir_empresas(df: pd.DataFrame):
    empresas_dict = {}

    for _, row in df.iterrows():
        empresa_nombre = str(row.get("Empresa", "")).strip()
        if not empresa_nombre:
            continue

        # Crear empresa si no existe
        if empresa_nombre not in empresas_dict:
            empresas_dict[empresa_nombre] = {
                "nombre": empresa_nombre,
                "sector": str(row.get("Sector", "")).strip(),
                "numero_empleados": to_int(row.get("NumEmpleadosEmpresa")),
                "empleados_sindicalizados": to_int(row.get("Sindicalizados")),
                "empleados_no_sindicalizados": to_int(row.get("NoSindicalizados")),
                "puestos": [],
                "prestaciones": {
                    "dias_adicionales": 0,
                    "dias_vacaciones": to_int(row.get("DiasVacaciones")),
                    "prima_vacacional": to_float(row.get("PrimaVacacional")),
                    "aguinaldo": to_int(row.get("Aguinaldo")),
                    "seguro_vida": to_bool(row.get("SeguroVida")),
                    "seguro_gastos_medicos": to_bool(row.get("SeguroGastosMedicos")),
                    "fondo_ahorro": to_bool(row.get("FondoAhorro")),
                    "bonos": to_bool(row.get("Bonos")),
                    "utilidades": to_bool(row.get("Utilidades")),
                    "comedor": to_bool(row.get("Comedor")),
                    "transporte": to_bool(row.get("Transporte")),
                    "vales": to_bool(row.get("Vales")),
                    "prevision_social": to_bool(row.get("PrevisionSocial"))
                },
                "rotacion": {
                    "anual": to_float(row.get("RotacionAnual")),
                    "30_dias": to_float(row.get("Rotacion30")),
                    "90_dias": to_float(row.get("Rotacion90")),
                    "180_dias": to_float(row.get("Rotacion180"))
                },
                "contrato_colectivo": {
                    "tiene": to_bool(row.get("TieneContrato")),
                    "sindicato": str(row.get("Sindicato", "")),
                    "aumento_salarial": to_float(row.get("AumentoSalarial"))
                }
            }

        # Agregar puesto
        puesto_nombre = str(row.get("Puesto", "")).strip()
        if puesto_nombre:
            empresas_dict[empresa_nombre]["puestos"].append({
                "nombre_puesto": puesto_nombre,
                "area": str(row.get("Area", "")).strip(),
                "empleados_en_puesto": to_int(row.get("EmpleadosPuesto")),
                "sueldo_bruto": to_float(row.get("SueldoBruto")),
                "sueldo_neto": to_float(row.get("SueldoNeto")),
                "sueldo_integrado": to_float(row.get("SueldoIntegrado"))
            })

    return list(empresas_dict.values())

# ==============================
# GUARDAR JSON
# ==============================

def guardar_json(empresas, path=OUTPUT_JSON):
    data = {"empresas": empresas}
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ==============================
# MAIN
# ==============================

def main():
    print("[INFO] Leyendo Excel...")
    df = leer_excel()

    print("[INFO] Construyendo estructura de empresas...")
    empresas = construir_empresas(df)

    print(f"[INFO] Empresas procesadas: {len(empresas)}")

    print("[INFO] Guardando JSON...")
    guardar_json(empresas)

    print(f"[OK] Archivo generado: {OUTPUT_JSON}")


if __name__ == '__main__':
    main()
