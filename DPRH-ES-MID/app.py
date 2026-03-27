import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("DPRH - Generador de Reportes")
        self.geometry("600x400")

        self.ruta_base = ""

        # Título
        self.label = ctk.CTkLabel(self, text="Sistema DPRH", font=("Arial", 20))
        self.label.pack(pady=20)

        # Botón seleccionar carpeta
        self.btn_select = ctk.CTkButton(
            self,
            text="Seleccionar carpeta raíz (Merida202X)",
            command=self.seleccionar_carpeta
        )
        self.btn_select.pack(pady=10)

        # Label ruta
        self.label_ruta = ctk.CTkLabel(self, text="Ninguna carpeta seleccionada")
        self.label_ruta.pack(pady=10)

        # Botón procesar
        self.btn_procesar = ctk.CTkButton(
            self,
            text="Generar Reporte",
            command=self.procesar
        )
        self.btn_procesar.pack(pady=20)

        # Barra de progreso
        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(pady=10, fill="x", padx=40)

        # Log
        self.log = ctk.CTkTextbox(self, height=120)
        self.log.pack(pady=10, fill="both", expand=True, padx=20)

    def log_msg(self, msg):
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.update()

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Selecciona carpeta raíz")

        if carpeta:
            self.ruta_base = carpeta
            self.label_ruta.configure(text=carpeta)
            self.log_msg(f"[INFO] Carpeta seleccionada: {carpeta}")

    def buscar_archivos(self):
        empresas = []

        for carpeta in os.listdir(self.ruta_base):
            ruta_empresa = os.path.join(self.ruta_base, carpeta)

            if os.path.isdir(ruta_empresa):
                archivos = os.listdir(ruta_empresa)

                excel = None
                dprh = None

                for a in archivos:
                    archivo_lower = a.lower()

                    # Detectar cualquier tipo de Excel
                    if archivo_lower.endswith((".xlsx", ".xls", ".xlsm")) and not archivo_lower.startswith("~$"):
                        excel = os.path.join(ruta_empresa, a)

                    # Detectar dprh
                    elif archivo_lower.endswith(".dprh"):
                        dprh = os.path.join(ruta_empresa, a)

                if excel:
                    empresas.append({
                        "nombre": carpeta,
                        "excel": excel,
                        "dprh": dprh
                    })
                    self.log_msg(f"[OK] {carpeta} → Excel encontrado")
                else:
                    self.log_msg(f"[WARN] {carpeta} → NO tiene Excel")

        return empresas
    def procesar(self):
        if not self.ruta_base:
            messagebox.showerror("Error", "Selecciona una carpeta primero")
            return

        self.progress.set(0)
        self.log_msg("[INFO] Buscando empresas...")

        empresas = self.buscar_archivos()

        total = len(empresas)

        if total == 0:
            messagebox.showerror("Error", "No se encontraron archivos")
            return

        self.log_msg(f"[INFO] Empresas encontradas: {total}")

        for i, e in enumerate(empresas):
            self.log_msg(f"[INFO] Procesando: {e['nombre']}")

            # Copiar Excel temporal
            os.system(
                f'copy "{e["excel"]}" input.xlsx'
                if os.name == 'nt'
                else f'cp "{e["excel"]}" input.xlsx'
            )

            # Ejecutar parser
            subprocess.run([sys.executable, "excel_parser.py"])

            # Aquí podrías usar el .dprh si lo necesitas

            progreso = (i + 1) / total
            self.progress.set(progreso)

        self.log_msg("[INFO] Generando PDF final...")

        subprocess.run([sys.executable, "pdf_generator_v2.py"])

        self.progress.set(1)

        messagebox.showinfo("Listo", "Reporte generado correctamente")


if __name__ == "__main__":
    app = App()
    app.mainloop()