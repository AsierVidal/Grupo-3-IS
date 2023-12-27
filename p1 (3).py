import tkinter as tk
from tkinter import filedialog, ttk
from leerbasededatosexcelycsv import read
from error_nan import crear_data_frame_entero, calcular_regresion2,escribir_ecuacion2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from clase_modelo import Modelo
import statsmodels.api as sm
import json
import pandas as pd

# Otras variables globales
colx_vars = []

tree_frame = None 
label_resultados = None 
ruta_modelo = None
canvas = None
frame_x = None
frame_y= None  
main_frame=None 




def on_canvas_y_configure(event):
    canvas_y.configure(scrollregion=canvas_y.bbox("all"))

def on_canvas_configure(event, canvas):
    if canvas and canvas.winfo_exists():
        canvas.configure(scrollregion=canvas.bbox("all"))

def on_main_frame_configure(event):
    canvas_main.configure(scrollregion=canvas_main.bbox("all"))

def cargar_y_visualizar_datos():
    global datos, ruta_archivo, tree_frame, tree, colx_vars, coly_var, frame_x, frame_y, root,canvas,main_frame

    # Limpiar la interfaz antes de cargar nuevos datos
    limpiar_interfaz()
    coly_var = None
    archivo = filedialog.askopenfilename(filetypes=[("CSV files", ".csv"), ("Excel files", ".xlsx;.xls"), ("All files", ".*")])
    if archivo:
        # Verificar si el archivo es un modelo guardado o un archivo de datos CSV/Excel
        if archivo.lower().endswith(('.csv', '.xlsx', '.xls')):
            # Cargar y visualizar datos CSV/Excel
            ruta_archivo.set(archivo)
            datos = read(archivo)
            ruta_modelo = None

        elif archivo.lower().endswith('.txt'):
            # Cargar un modelo previamente guardado
            ruta_modelo = archivo  # Almacenar la ruta del modelo
            cargar_modelo(archivo)


    
        # Agregar un Canvas para permitir el desplazamiento vertical
        canvas_main = tk.Canvas(root,width=750, height=750)
        canvas_main.grid(row=20, column=0, sticky="nsew")

        # Crear el marco principal para contener todos los elementos
        main_frame = tk.Frame(canvas_main, width=750, height=750)
        main_frame.grid(row=20, column=0, sticky="nsew")
        
        

         # Configurar el área de desplazamiento vertical para el Canvas
        scrollbar_y_main = ttk.Scrollbar(root, orient="vertical", command=canvas_main.yview)
        scrollbar_y_main.grid(row=2, column=1, sticky="ns")

        # Configurar el Canvas para usar la barra de desplazamiento vertical
        canvas_main.config(yscrollcommand=scrollbar_y_main.set)
            # Mostrar el Treeview en el Canvas
        canvas_main.create_window((0, 0), window=main_frame, anchor="nw")

    
        # Configurar el evento para ajustar el área de desplazamiento cuando cambie el tamaño del lienzo
        canvas_main.bind("<Configure>", lambda event, canvas=canvas: on_canvas_configure(event, canvas))

        
        # Crear el marco para el Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        # Crear la barra de desplazamiento horizontal
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.grid(row=4, column=0, sticky="ew")
        
        # Crear un Canvas para permitir el desplazamiento
        canvas = tk.Canvas(tree_frame, width=700, height=240, xscrollcommand=scrollbar_x.set)
        canvas.grid(row=2, column=0, sticky="nsew")

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
        canvas.bind("<Configure>", lambda event, canvas=canvas: on_canvas_configure(event, canvas))

        # Configurar la barra de desplazamiento horizontal
        scrollbar_x.config(command=canvas.xview)
        canvas.config(xscrollcommand=scrollbar_x.set)

        # Configurar la barra de desplazamiento vertical para el Treeview en el Canvas
        scrollbar_y_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar_y_tree.grid(row=2, column=1, sticky="ns")

        # Configurar el área de desplazamiento para la barra de desplazamiento vertical del Treeview
        tree.config(yscrollcommand=scrollbar_y_tree.set)

      

        # Configurar el evento para ajustar el área de desplazamiento cuando cambie el tamaño de la ventana principal
        root.bind("<Configure>", lambda event, canvas=canvas: on_canvas_configure(event, canvas))

          # Ajusta las coordenadas según tus necesidades
        tree_frame.place(x=0, y=0)

        # Configurar el tamaño mínimo de la ventana
        root.minsize(200, 200)

      

        # Crear checkboxes para seleccionar múltiples columnas X
        coly_var = tk.StringVar()
        coly_var.set(datos.columns[0])  # Establecer el valor predeterminado como la primera columna

        # Contenedor para las columnas X
        frame_x = tk.Frame(main_frame)
        frame_x.place(x=150, y=300)

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
        frame_y = tk.Frame(main_frame)
        frame_y.place(x=150, y=350)

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

      
        # Configurar el área de desplazamiento para la barra de desplazamiento vertical del Treeview
        tree.config(yscrollcommand=scrollbar_y_tree.set)

        # Configurar el tamaño mínimo de la ventana principal
        root.update_idletasks()
        root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())

        # Configurar el evento para ajustar el área de desplazamiento cuando cambie el tamaño de la ventana principal
        root.bind("<Configure>", lambda event, canvas=canvas: on_canvas_configure(event,canvas))

 
 
       
def limpiar_interfaz():
    global tree_frame, cargar_regresion, guardar_boton, label_resultados, canvas, frame_x, frame_y,canvas,root

    # Eliminar gráficas anteriores
    if canvas and canvas.winfo_exists():
        
        bbox_result = canvas.bbox("all")
        canvas = None
    # Resto del código que usa bbox_result

    # Destruir el marco del Treeview si existe
    if tree_frame is not None:
        tree_frame.destroy()
        tree_frame = None  # Establecer tree_frame a None después de destruirlo

    if frame_x is not None:
        frame_x.destroy()
        frame_x = None

    if frame_y is not None:
        frame_y.destroy()
        frame_y = None

    if cargar_regresion is not None and cargar_regresion.winfo_exists():
        cargar_regresion.grid_remove()


    if guardar_boton is not None:
        guardar_boton.grid_remove()

    # Destruir el label de resultados si existe
    if label_resultados is not None:
        label_resultados.destroy()
        label_resultados = None  # Establecer label_resultados a None después de destruirlo

    # Borrar el label anterior, si existe
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()

     
def columnas_seleccionadas():
    global colx_vars, coly_var, cargar_regresion, cargar_boton

    # Implementa la lógica para verificar si se han seleccionado columnas
    columnas_x_seleccionadas = [col for col, var in colx_vars if var.get()]
    if columnas_x_seleccionadas and coly_var.get():
        # Al menos una columna X y una columna Y están seleccionadas
        cargar_regresion.grid(row=30, column=10, columnspan=1, pady=10, sticky="nsew")
        

    else:
        # No hay columnas X o no hay columna Y seleccionada
        cargar_regresion.place_forget()

def mostrar_interfaz_grafica():
    global cargar_regresion, cargar_boton, modelo_g, label_resultados

    # Mostrar el botón de graficar y guardar
    guardar_boton.place(x=600, y=350)

def guardar_modelo():
    global modelo_g

    # Utilizar un cuadro de diálogo para obtener la ruta del archivo
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", ".txt"), ("All files", ".*")])

    # Guardar el modelo en un archivo
    if ruta_archivo:
        modelo_g.guardar_modelo(ruta_archivo)


def creador_de_modelo():
    global datos, colx_vars, coly_var, root, modelo_g
    
    # Obtener las columnas seleccionadas
    columnas_x_seleccionadas = [col for col, var in colx_vars if var.get()]
    columna_y_seleccionada = coly_var.get()

    

    if columnas_x_seleccionadas and columna_y_seleccionada:
        # Aquí puedes realizar las operaciones para calcular la regresión utilizando las columnas seleccionadas
        modelo_g = calcular_regresion2(datos, columnas_x_seleccionadas, columna_y_seleccionada)
        text = escribir_ecuacion2(modelo_g)

        # Crear el label sin colocarlo inmediatamente
        label_resultados = tk.Label(main_frame, text=text)
        label_resultados.update_idletasks()  # Asegura que las medidas se actualicen
 

        # Colocar el label en el centro horizontal
        label_resultados.place(x=250 ,y=430)

        grafica_modelo()
        mostrar_interfaz_grafica()

def grafica_modelo():
    global datos, canvas
    if datos is not None:
        # Selecciona las columnas X e Y
        columnas_x_seleccionadas = [col for col, var in colx_vars if var.get()]
        columna_y_seleccionada = coly_var.get()

        if columnas_x_seleccionadas and columna_y_seleccionada:
            # Aquí se integra la función crear_data_frame_entero para manejar NaN
            x = crear_data_frame_entero(datos[columnas_x_seleccionadas])
            y = datos[columna_y_seleccionada]
            
            # Divide los datos en conjuntos de entrenamiento y prueba
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

            # Crea un modelo de regresión lineal
            modelo = LinearRegression()

            # Entrena el modelo con los datos de entrenamiento
            modelo.fit(x_train, y_train)

            # Realiza predicciones con los datos de prueba
            y_pred = modelo.predict(x_test)

            # Crea la gráfica de regresión lineal
            plt.figure(figsize=(6, 4))
            plt.scatter(x_test.iloc[:, 0], y_test, color='black')  # Solo se muestra la primera columna X para la gráfica
            plt.plot(x_test.iloc[:, 0], y_pred, color='blue', linewidth=3)
            plt.title('Regresión Lineal')
            plt.xlabel(", ".join(columnas_x_seleccionadas))
            plt.ylabel(columna_y_seleccionada)

            # Integra la gráfica en la ventana principal
            canvas = FigureCanvasTkAgg(plt.gcf(), master=main_frame)
            canvas.draw()
            canvas.get_tk_widget().place(x=80, y=480)  # Ajusta el valor de padx según tus necesidades

def cargar_modelo():
    global ruta_modelo, cargar_regresion, guardar_boton, label_resultados

    # Limpiar la interfaz antes de cargar un modelo
    limpiar_interfaz()
 
    # Abrir el cuadro de diálogo para seleccionar un archivo
    ruta_modelo = filedialog.askopenfilename(filetypes=[("Text files", ".txt"), ("All files", ".*")])

    # Verificar si se ha seleccionado un modelo
    if not ruta_modelo:
        return None

    try:
        print(f"Ruta del archivo: {ruta_modelo}")

        with open(ruta_modelo, 'r', encoding='utf-8') as archivo:
            contenido_json = json.load(archivo)

        print("Contenido JSON cargado:", contenido_json)

        # Mostrar la información del modelo en la interfaz
        mostrar_info_modelo(contenido_json)

    except Exception as e:
        print(f"Error al cargar el modelo desde {ruta_modelo}: {e}")
        traceback.print_exc()  # Imprimir el traceback completo

   

def mostrar_info_modelo(modelo_data):
    global label_resultados

    # Lógica para mostrar la información del modelo en la interfaz
    if "parametros_ajuste" in modelo_data and "cols_x_dict" in modelo_data and "coly" in modelo_data and "const" in modelo_data:
        modelo_g = Modelo(
            nombre=modelo_data["nombre"],
            descripcion=modelo_data["descripcion"],
            parametros_ajuste=modelo_data["parametros_ajuste"],
            cols_x_dict=modelo_data["cols_x_dict"],
            coly=modelo_data["coly"],
            const=modelo_data["const"]
        )

        text = escribir_ecuacion2(modelo_g)
        label_resultados = tk.Label(main_frame, text=text)
        label_resultados.place(x=200, y=100)  # Ajusta las coordenadas según tus necesidades
    else:
        print("Datos de modelo incompletos.")


# Configuración de la ventana principal
root = tk.Tk()

screen_height = root.winfo_screenheight()

# Define la posición x en 750
x_position = 750

# Calcula la posición y centrada verticalmente
# Configura la posición de la ventana
root.geometry(f"750x{screen_height}+{x_position}+0")

root.title('Aplicación de Regresión Lineal')
root.resizable(width=True, height=True)

ruta_archivo = tk.StringVar()

ruta_entry = tk.Entry(main_frame, textvariable=ruta_archivo, state="readonly", width=80)
ruta_entry.place(x=10, y=10)

examinar_button = tk.Button(main_frame, text='Examinar', command=lambda: cargar_y_visualizar_datos())
examinar_button.place(x=530, y=5)



# Crear el botón "Cargar Modelo"
cargar_boton = tk.Button(root, text='Cargar Modelo', command=lambda: cargar_modelo())
cargar_boton.place(x=600, y=5)

button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=3, pady=10)

# Botón "Hacer Regresión"
cargar_regresion = tk.Button(root, text='Hacer Regresión', command=creador_de_modelo)
cargar_regresion.grid(row=30, column=10, columnspan=1, pady=10, sticky="nsew")
cargar_regresion.grid_remove()

# Crear el botón "Guardar Modelo"
guardar_boton = tk.Button(root, text='Guardar Modelo', command=guardar_modelo)
guardar_boton.grid(row=8, column=0, columnspan=1, padx=10, sticky="nsew")
guardar_boton.grid_remove()



root.mainloop()