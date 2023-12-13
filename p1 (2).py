import tkinter as tk
from tkinter import filedialog, ttk
from leerbasededatosexcelycsv import read
from error_nan import crear_data_frame_entero, calcular_regresion2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
colx_vars = []
coly_var = None
def on_canvas_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))
def cargar_y_visualizar_datos():
    global datos, ruta_archivo, tree_frame, tree, colx_vars, coly_var
    archivo = filedialog.askopenfilename()
    if archivo:
        ruta_archivo.set(archivo)
        datos = read(archivo)
        # Mostrar las columnas en la consola
        print("Columnas disponibles:")
        print(datos.columns)
        # Crear el marco para el Treeview
        tree_frame = ttk.Frame(root)
        tree_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
        
        # Crear la barra de desplazamiento horizontal
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        # Crear un Canvas para permitir el desplazamiento
        canvas = tk.Canvas(tree_frame, width=700, height=240, xscrollcommand=scrollbar_x.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        # Crear el Treeview sin altura fija
        tree = ttk.Treeview(canvas, columns=tuple(datos.columns))
        # Configurar el ancho de la columna del índice
        tree.column("#0", width=50, anchor=tk.CENTER)
        # Configurar el ancho de las columnas
        for col in datos.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        # Insertar los datos en el Treeview
        for i, row in datos.iterrows():
            tree.insert("", i, text=str(i), values=tuple(row))
        # Mostrar el Treeview en el Canvas
        canvas.create_window((0, 0), window=tree, anchor="nw")
 
 
        # Configurar el evento para ajustar el área de desplazamiento cuando cambie el tamaño del lienzo
        canvas.bind("<Configure>", lambda event, canvas=canvas: on_canvas_configure(canvas))
        # Configurar la barra de desplazamiento horizontal
        scrollbar_x.config(command=canvas.xview)
        canvas.config(xscrollcommand=scrollbar_x.set)
        # Configurar el tamaño mínimo de la ventana
        root.minsize(200, 200)
      
        # Crear checkboxes para seleccionar múltiples columnas X
        coly_var = tk.StringVar()
        coly_var.set(datos.columns[0])  # Establecer el valor predeterminado como la primera columna
        # Contenedor para las columnas X
        frame_x = tk.Frame(root)
        frame_x.place(x=150, y=310)
        label_x = tk.Label(frame_x, text="Columna X")
        label_x.grid(row=1, column=0)
        canvas_x = tk.Canvas(frame_x, height=30)
        canvas_x.grid(row=1, column=2)
        inner_frame_x = tk.Frame(canvas_x)
        canvas_x.create_window((0, 0), window=inner_frame_x, anchor="nw")
        # Lista para almacenar las variables de las casillas de verificación de las columnas X
        colx_vars = []
        for i, col in enumerate(datos.columns):
            var = tk.BooleanVar()
            colx_vars.append((col, var))
            checkbox_x = tk.Checkbutton(inner_frame_x, text=col, variable=var, command=columnas_seleccionadas)
            checkbox_x.grid(row=0, column=i, sticky="w")
        inner_frame_x.update_idletasks()
        canvas_x.configure(scrollregion=canvas_x.bbox("all"))
        # Añadir barra de desplazamiento horizontal para Columna X
        scrollbar_x = ttk.Scrollbar(frame_x, orient="horizontal", command=canvas_x.xview)
        scrollbar_x.grid(row=2, column=1, columnspan=len(datos.columns), sticky="ew")
        canvas_x.configure(xscrollcommand=scrollbar_x.set)
        # Contenedor para la columna Y
        frame_y = tk.Frame(root)
        frame_y.place(x=150, y=370)
        label_y = tk.Label(frame_y, text="Columna Y")
        label_y.grid(row=1, column=0)
        canvas_y = tk.Canvas(frame_y, height=30)
        canvas_y.grid(row=1, column=1)
        inner_frame_y = tk.Frame(canvas_y)
        canvas_y.create_window((0, 0), window=inner_frame_y, anchor="nw")
        for i, col in enumerate(datos.columns):
            radio_button_y = tk.Radiobutton(inner_frame_y, text=col, variable=coly_var, value=col)
            radio_button_y.grid(row=0, column=i, sticky="w")
        inner_frame_y.update_idletasks()
        canvas_y.configure(scrollregion=canvas_y.bbox("all"))
        # Añadir barra de desplazamiento horizontal para Columna Y
        scrollbar_y = ttk.Scrollbar(frame_y, orient="horizontal", command=canvas_y.xview)
        scrollbar_y.grid(row=2, column=1, columnspan=len(datos.columns), sticky="ew")
        canvas_y.configure(xscrollcommand=scrollbar_y.set)
        
def columnas_seleccionadas():
    global colx_vars, coly_var, cargar_regresion, cargar_boton
    # Implementa la lógica para verificar si se han seleccionado columnas
    columnas_x_seleccionadas = [col for col, var in colx_vars if var.get()]
    if columnas_x_seleccionadas and coly_var.get():
        # Al menos una columna X y una columna Y están seleccionadas
        cargar_regresion.place(x=620, y=340)
        cargar_boton.place(x=620, y=380)
    else:
        # No hay columnas X o no hay columna Y seleccionada
        cargar_regresion.place_forget()
        cargar_boton.place_forget()
def creador_de_modelo():
    global datos, colx_vars, coly_var, root, modelos_guardados, modelo_g
    # Obtener las columnas seleccionadas
    columnas_x_seleccionadas = [col for col, var in colx_vars if var.get()]
    columna_y_seleccionada = coly_var.get()
    # Mostrar las columnas X e Y en la consola
    print(f"Se han seleccionado las columnas X: {columnas_x_seleccionadas}")
    print(f"Se ha seleccionado la columna Y: {columna_y_seleccionada}")
    if columnas_x_seleccionadas and columna_y_seleccionada:
        # Aquí puedes realizar las operaciones para calcular la regresión utilizando las columnas seleccionadas
        modelo_g = calcular_regresion2(datos, columnas_x_seleccionadas, columna_y_seleccionada)


        label_resultados = tk.Label(root, text=f"R^2: {modelo_g[3][0]}, Condición: {modelo_g[3][1]}")
        label_resultados.place(x=260,y=430)