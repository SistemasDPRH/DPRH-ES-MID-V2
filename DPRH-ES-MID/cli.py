import argparse
import subprocess
import sys
import os

"""
CLI para ejecutar todo el pipeline DPRH desde un solo comando.

Uso:
    python cli.py input.xlsx

Flujo:
    1. Excel -> JSON (excel_parser.py)
    2. JSON -> PDF (pdf_generator_v2.py)
"""

# ==============================
# FUNCIONES
# ==============================

def ejecutar_comando(comando):
    try:
        result = subprocess.run(comando, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falló el comando: {comando}")
        print(e)
        return False


def validar_archivo(path):
    if not os.path.exists(path):
        print(f"[ERROR] El archivo no existe: {path}")
        sys.exit(1)

# ==============================
# MAIN
# ==============================

def main():
    parser = argparse.ArgumentParser(description="Generador DPRH desde Excel a PDF")
    parser.add_argument("excel", help="Ruta del archivo Excel (input.xlsx)")

    args = parser.parse_args()

    excel_path = args.excel

    print("\n[INFO] Iniciando proceso DPRH...")

    # Validar archivo
    validar_archivo(excel_path)

    # Copiar nombre esperado
    print("[INFO] Preparando archivo Excel...")
    os.system(f"copy \"{excel_path}\" input.xlsx" if os.name == 'nt' else f"cp '{excel_path}' input.xlsx")

    # Paso 1: Excel -> JSON
    print("[INFO] Ejecutando parser de Excel...")
    if not ejecutar_comando([sys.executable, "excel_parser.py"]):
        sys.exit(1)

    # Paso 2: Generar PDF
    print("[INFO] Generando PDF...")
    if not ejecutar_comando([sys.executable, "pdf_generator_v2.py"]):
        sys.exit(1)

    print("\n[OK] Proceso completado correctamente")
    print("Archivo generado: reporte_dprh_v2.pdf")


if __name__ == '__main__':
    main()
