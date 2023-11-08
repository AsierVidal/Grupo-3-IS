import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Declara datos como variable global
datos = None

# Variables para almacenar las columnas X
colx_entries = []

def crear_modelo_regresion():
    # Función para mostrar los campos de entrada y opciones para el modelo de regresión
    nombre_modelo_label.pack()
    nombre_modelo_entry.pack()
    colx_label.pack()
    colx_entry_widget.pack()
    agregar_colx_button.pack()
    coly_label.pack()
    coly_entry_widget.pack()
    crear_modelo_boton.config(state="disabled")

def agregar_columna_x():
    colx = colx_entry_widget.get()
    colx_entries.append(colx)
    colx_entry_widget.delete(0, tk.END)
    if tk.messagebox.askyesno("Pregunta", "¿Desea agregar más columnas X?"):
        colx_label.config(text="Columna X:")
    else:
        colx_label.config(text="Columnas X:")
        colx_entry_widget.config(state="disabled")
        agregar_colx_button.config(state="disabled")

def calcular_regresion():
    pass

def guardar_modelo():
    pass

def cargar_modelo(archivo):
   pass

def cargar_y_visualizar_datos():
    archivo = filedialog.askopenfilename()
    if archivo:
        ruta_archivo.set(archivo)

def hacer_predicción():
    pass

root = tk.Tk()
root.geometry("400x400")
root.title('Aplicación de Regresión Lineal')
root.resizable(width=False, height=False)

# Etiqueta para mostrar la ruta del archivo
ruta_archivo = tk.StringVar()
ruta_label = tk.Label(root, text="Ruta del archivo:")
ruta_label.pack(pady=10)
ruta_entry = tk.Entry(root, textvariable=ruta_archivo, state="readonly", width=40)
ruta_entry.pack(pady=5)

# Botón para cargar datos
file_button = tk.Button(root, text='Cargar Datos', command=cargar_y_visualizar_datos)
file_button.pack(pady=10)

# Campos de entrada y botón para crear el modelo de regresión
nombre_modelo_label = tk.Label(root, text="Nombre del Modelo:")
nombre_modelo_entry = tk.Entry(root)
colx_label = tk.Label(root, text="Columnas X:")
colx_entry_widget = tk.Entry(root)
agregar_colx_button = tk.Button(root, text="Agregar Columna X", command=agregar_columna_x)
coly_label = tk.Label(root, text="Columna Y:")
coly_entry_widget = tk.Entry(root)

crear_modelo_boton = tk.Button(root, text='Crear Modelo de Regresión', command=crear_modelo_regresion)
crear_modelo_boton.pack(pady=10)

# Cuadro de botones para operaciones
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

guardar_boton = tk.Button(button_frame, text='Guardar Modelo', command=guardar_modelo)
cargar_boton = tk.Button(button_frame, text='Cargar Modelo', command=cargar_modelo)
boton_predicción = tk.Button(button_frame, text='Hacer Predicción', command=hacer_predicción)

guardar_boton.pack(side=tk.LEFT, padx=10)
cargar_boton.pack(side=tk.LEFT, padx=10)
boton_predicción.pack(side=tk.LEFT, padx=10)

root.mainloop()
