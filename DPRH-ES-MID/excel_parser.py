import pandas as pd
import json

# ==============================
# CONFIG
# ==============================

EXCEL_PATH = "input.xlsx"
OUTPUT_JSON = "empresas.json"

# ==============================
# UTILIDADES
# ==============================

def obtener_hoja(path):
    xls = pd.ExcelFile(path)
    return xls.sheet_names[0]  # usa la primera hoja

def limpiar_texto(s):
    if pd.isna(s):
        return ""
    return str(s).strip()


def to_bool(val):
    if pd.isna(val):
        return False
    val = str(val).strip().lower()
    return val in ["1", "true", "si", "sí", "yes", "x"]


def to_float(val):
    if pd.isna(val):
        return 0.0
    try:
        return float(str(val).replace(",", "").replace("$", ""))
    except:
        return 0.0


def to_int(val):
    if pd.isna(val):
        return 0
    try:
        return int(float(val))
    except:
        return 0

# ==============================
# EXTRAER NOMBRE EMPRESA
# ==============================

def obtener_nombre_empresa(path):
    try:
        sheet = obtener_hoja(path)
        df = pd.read_excel(path, sheet_name=sheet, header=None)

        for i in range(len(df)):
            val = str(df.iloc[i, 0]).lower()
            if "nombre de la empresa" in val:
                return str(df.iloc[i, 2]).strip()

    except Exception as e:
        print(f"[WARN] No se pudo leer nombre empresa: {e}")

    return "Empresa"

# ==============================
# LEER EXCEL REAL
# ==============================

def leer_excel(path):
    print("[INFO] Leyendo Excel...")

    sheet = obtener_hoja(path)

    # Intentar diferentes filas como encabezado
    for header_row in [2, 3, 4, 5]:
        try:
            df = pd.read_excel(path, sheet_name=sheet, header=header_row)

            df = df.dropna(axis=1, how='all')
            df.columns = [str(c).strip() for c in df.columns]

            # Validar si parece tabla real
            columnas = " ".join(df.columns).lower()

            if "puesto" in columnas or "sueldo" in columnas:
                print(f"[OK] Header detectado en fila {header_row}")
                print(df.columns.tolist())
                return df

        except:
            continue

    print("[WARN] No se pudo detectar estructura válida")
    return pd.DataFrame()

# ==============================
# MAPEO FLEXIBLE
# ==============================

def obtener_columna(df, posibles_nombres):
    for nombre in posibles_nombres:
        for col in df.columns:
            if nombre.lower() in col.lower():
                return col
    return None

# ==============================
# CONSTRUIR EMPRESA
# ==============================

def construir_empresas(df, nombre_empresa):
    empresas = []

    sector_col = obtener_columna(df, ["sector"])
    puesto_col = obtener_columna(df, ["puesto"])
    area_col = obtener_columna(df, ["area"])
    empleados_puesto_col = obtener_columna(df, ["empleados"])
    bruto_col = obtener_columna(df, ["bruto"])
    neto_col = obtener_columna(df, ["neto"])
    integrado_col = obtener_columna(df, ["integrado"])

    empresa = {
        "nombre": nombre_empresa,
        "sector": limpiar_texto(df[sector_col].iloc[0]) if sector_col else "",
        "numero_empleados": 0,
        "empleados_sindicalizados": 0,
        "empleados_no_sindicalizados": 0,
        "puestos": [],
        "prestaciones": {
            "dias_adicionales": 0,
            "dias_vacaciones": 0,
            "prima_vacacional": 0,
            "aguinaldo": 0,
            "seguro_vida": False,
            "seguro_gastos_medicos": False,
            "fondo_ahorro": False,
            "bonos": False,
            "utilidades": False,
            "comedor": False,
            "transporte": False,
            "vales": False,
            "prevision_social": False
        },
        "rotacion": {
            "anual": 0,
            "30_dias": 0,
            "90_dias": 0,
            "180_dias": 0
        },
        "contrato_colectivo": {
            "tiene": False,
            "sindicato": "",
            "aumento_salarial": 0
        }
    }

    for _, row in df.iterrows():
        puesto = limpiar_texto(row.get(puesto_col))
        if not puesto:
            continue

        empresa["puestos"].append({
            "nombre_puesto": puesto,
            "area": limpiar_texto(row.get(area_col)),
            "empleados_en_puesto": to_int(row.get(empleados_puesto_col)),
            "sueldo_bruto": to_float(row.get(bruto_col)),
            "sueldo_neto": to_float(row.get(neto_col)),
            "sueldo_integrado": to_float(row.get(integrado_col))
        })

    empresas.append(empresa)
    return empresas

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
    nombre_empresa = obtener_nombre_empresa(EXCEL_PATH)

    df = leer_excel(EXCEL_PATH)

    print("[INFO] Construyendo empresa...")
    empresas = construir_empresas(df, nombre_empresa)

    print(f"[INFO] Empresas procesadas: {len(empresas)}")

    guardar_json(empresas)

    print("[OK] JSON generado correctamente")

if __name__ == '__main__':
    main()