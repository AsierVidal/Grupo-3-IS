import tkinter as tk
from tkinter import filedialog, messagebox
from leerbasededatosexcelycsv import read

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("Aplicación de regresión lineal")
        master.geometry("600x600")  # Establecer un tamaño fijo

        self.label = tk.Label(master, text="Aplicación de regresión lineal")
        self.label.pack(pady=20)

        self.examinar_button = tk.Button(master, text="Examinar", command=self.examinar_archivo)
        self.examinar_button.pack()

        self.cargar_modelo_button = tk.Button(master, text="Cargar modelo", command=self.cargar_modelo)
        self.cargar_modelo_button.pack()

    def examinar_archivo(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos de Excel y CSV", "*.xls;*.xlsx;*.csv")])
        if file_path:
            try:
                import pandas as pd
                data = read(file_path)
                columnas = list(data.columns)

                # Mostrar un cuadro de diálogo múltiple para seleccionar columnas
                col_x = []
                dialogo = tk.Toplevel(self.master)
                dialogo.title("Seleccionar columnas")
                dialogo.geometry("600x600")  # Establecer un tamaño fijo

                for columna in columnas:
                    var = tk.BooleanVar(value=True)
                    checkbutton = tk.Checkbutton(dialogo, text=columna, variable=var)
                    checkbutton.pack(anchor=tk.W)
                    col_x.append((columna, var))

                confirmar_button = tk.Button(dialogo, text="Confirmar", command=lambda: self.obtener_seleccion_columnas(col_x, dialogo))
                confirmar_button.pack()

            except Exception as e:
                messagebox.showerror("Error", f"Error al leer el archivo: {str(e)}")

    def obtener_seleccion_columnas(self, seleccion_columnas, dialogo):
        columnas_seleccionadas = [opcion for opcion, var in seleccion_columnas if var.get()]
        dialogo.destroy()
        messagebox.showinfo("Columnas seleccionadas", f"Columnas seleccionadas: {columnas_seleccionadas}")

    def cargar_modelo(self):
        # Aquí puedes agregar la lógica para cargar un modelo
        messagebox.showinfo("Cargar Modelo", "Funcionalidad para cargar modelo aún no implementada")

# Crear la ventana principal
root = tk.Tk()
app = VentanaPrincipal(root)

# Iniciar el bucle de eventos
root.mainloop()
