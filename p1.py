import tkinter as tk
from tkinter import filedialog, ttk
from leerbasededatosexcelycsv import read
from error_nan import crear_data_frame_entero, calcular_regresion2, escribir_ecuacion2, predecir_nuevos_valores
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from clase_modelo import Modelo
import statsmodels.api as sm
import numpy as np
import ast
import pandas as pd

# Otras variables globales
colx_vars = []
coly_var = None
tree_frame = None 
label_resultados = None 
ruta_modelo = None
canvas = None
frame_x = None
frame_y=None  # Agrega esta línea para definir frame_x como variable global
label_resultados = None
guardar_boton = None
label_grafica = None
frame_prediccion = None
entradas_prediccion = []
datos_prediccion = []



def on_canvas_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def cargar_y_visualizar_datos():
    global datos, ruta_archivo, tree_frame, tree, colx_vars, coly_var,frame_x,frame_y

    # Limpiar la interfaz antes de cargar nuevos datos
    limpiar_interfaz()

    archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")])
    if archivo:
        # Verificar si el archivo es un modelo guardado o un archivo de datos CSV/Excel
        if archivo.lower().endswith(('.csv', '.xlsx', '.xls')):
            # Cargar y visualizar datos CSV/Excel
            ruta_archivo.set(archivo)
            datos = read(archivo)
            ruta_modelo=None

        elif archivo.lower().endswith('.txt'):
            # Cargar un modelo previamente guardado
            ruta_modelo = archivo  # Almacenar la ruta del modelo
            cargar_modelo(archivo)

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

def limpiar_interfaz():
    global tree_frame, cargar_regresion, guardar_boton, label_resultados, canvas, frame_x, frame_y, frame_prediccion

    # Eliminar gráficas anteriores
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None

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

    # Ocultar el botón de regresión y el botón de guardar
    if cargar_regresion is not None:
        cargar_regresion.place_forget()
    
    if guardar_boton is not None:
        guardar_boton.place_forget()

    # Destruir el label de resultados si existe
    if label_resultados is not None:
        label_resultados.destroy()
        label_resultados = None  # Establecer label_resultados a None después de destruirlo
    
    if frame_prediccion is not None:
        frame_prediccion.destroy()
        frame_prediccion = None

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
        cargar_regresion.place(x=620, y=340)
    else:
        # No hay columnas X o no hay columna Y seleccionada
        cargar_regresion.place_forget()

def mostrar_interfaz_grafica():
    global cargar_regresion, cargar_boton, modelo_g, label_resultados

    # Mostrar el botón de graficar y ocultar el botón de guardar
    guardar_boton.place(x=620, y=430)
     
     
     

    

def obtener_datos_adicionales():
    # Crea una nueva ventana emergente
    ventana_datos = tk.Toplevel(root)
    ventana_datos.title("Nombre y Descripción del modelo a guardar")

    # Agrega etiquetas y cuadros de texto para obtener los datos
    tk.Label(ventana_datos, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
    dato1_var = tk.StringVar()
    dato1_entry = tk.Entry(ventana_datos, textvariable=dato1_var)
    dato1_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana_datos, text="Descripción:").grid(row=1, column=0, padx=10, pady=5)
    dato2_var = tk.StringVar()
    dato2_entry = tk.Entry(ventana_datos, textvariable=dato2_var)
    dato2_entry.grid(row=1, column=1, padx=10, pady=5)

    # Función para obtener datos y luego llamar a guardar_modelo
    def obtener_datos_y_guardar_modelo():
        dato1 = dato1_var.get()
        dato2 = dato2_var.get()
        ventana_datos.destroy()
        guardar_modelo(dato1, dato2)

    # Botón para confirmar y cerrar la ventana
    tk.Button(ventana_datos, text="Guardar", command=obtener_datos_y_guardar_modelo).grid(row=2, column=0, columnspan=2, pady=10)

def guardar_modelo(nombre, descripcion):
    global modelo_g
    modelo_g.set_nombre(nombre)
    modelo_g.set_descripcion(descripcion)
    # Utilizar un cuadro de diálogo para obtener la ruta del archivo
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # Guardar el modelo en un archivo
    if ruta_archivo:
        modelo_g.guardar_modelo(ruta_archivo)



def creador_de_modelo(cargar = None):
    global datos, colx_vars, coly_var, root, modelo_g, canvas, label_resultados, label_grafica, modelo_resultado, entradas_prediccion, frame_prediccion
    # Oculta el botón "Guardar modelo" si existe
    if guardar_boton:
        guardar_boton.place_forget()
    
    if label_resultados:
        label_resultados.destroy()   

    # Destruye la gráfica anterior si existe
    if canvas:
        canvas.get_tk_widget().destroy()

    if label_grafica:
        label_grafica.destroy()

    # if frame_prediccion:
    #     frame_prediccion.destroy()

    if cargar == None:
        
        # Obtener las columnas seleccionadas
        columnas_x_seleccionadas = [col for col, var in colx_vars if var.get()]
        columna_y_seleccionada = coly_var.get()

        if columnas_x_seleccionadas and columna_y_seleccionada:
            
            # Aquí puedes realizar las operaciones para calcular la regresión utilizando las columnas seleccionadas
            try:
                modelo_g, modelo_resultado = calcular_regresion2(datos, columnas_x_seleccionadas, columna_y_seleccionada)
                text = escribir_ecuacion2(modelo_g)
                
                # Crear el label sin colocarlo inmediatamente
                label_resultados = tk.Label(root, text=text)
                label_resultados.update_idletasks()  # Asegura que las medidas se actualicen

                # Calcular la posición para centrar horizontalmente
                x_position = (root.winfo_width() - label_resultados.winfo_reqwidth()) / 2

                # Colocar el label en el centro horizontal
                label_resultados.place(x=x_position, y=430)

                # Graficar el modelo
                grafica_modelo()
                mostrar_interfaz_grafica()
                
                # Crear cuadros de entrada para la predicción
                frame_prediccion = tk.Frame(root)
                frame_prediccion.place(x=250, y=500)  # Ajusta la posición según tus necesidades

                tk.Label(frame_prediccion, text="Ingrese los valores para la predicción:").grid(row=0, column=0, columnspan=2)

                entradas_prediccion = []
                for i, col in enumerate(columnas_x_seleccionadas):
                    tk.Label(frame_prediccion, text=f"{col}:").grid(row=i + 1, column=0)
                    valor_var = tk.DoubleVar()
                    entry_valor = tk.Entry(frame_prediccion, textvariable=valor_var)
                    entry_valor.grid(row=i + 1, column=1)
                    entradas_prediccion.append(valor_var)

                # Botón para realizar la predicción
                tk.Button(frame_prediccion, text='Realizar Predicción', command=realizar_prediccion).grid(row=len(columnas_x_seleccionadas) + 1, column=0, columnspan=2, pady=10)

                

            except ValueError:
                text = 'Una de las columnas seleccionadas no tiene todos los datos en formato numérico'

                label_resultados = tk.Label(root, text=text)
                label_resultados.update_idletasks()  # Asegura que las medidas se actualicen

                # Calcular la posición para centrar horizontalmente
                x_position = (root.winfo_width() - label_resultados.winfo_reqwidth()) / 2

                # Colocar el label en el centro horizontal
                label_resultados.place(x=x_position, y=430)
    elif cargar == 'si':
        
        # Obtener las columnas seleccionadas
        columnas_x_seleccionadas = []
        for k in modelo_g.cols_x_dict.keys():
            columnas_x_seleccionadas.append(k)
        columna_y_seleccionada = modelo_g.coly

        if columnas_x_seleccionadas and columna_y_seleccionada:
            # Aquí puedes realizar las operaciones para calcular la regresión utilizando las columnas seleccionadas
            try:
                text = escribir_ecuacion2(modelo_g)

                # Crear el label sin colocarlo inmediatamente
                label_resultados = tk.Label(root, text=text)
                label_resultados.update_idletasks()  # Asegura que las medidas se actualicen

                # Calcular la posición para centrar horizontalmente
                x_position = (root.winfo_width() - label_resultados.winfo_reqwidth()) / 2

                # Colocar el label en el centro horizontal
                label_resultados.place(x=x_position, y=150)
                 
                # Graficar el modelo
                guardar_boton.place(x=620,y=150)
            
            except ValueError:
                text = 'Una de las columnas seleccionadas no tiene todos los datos en formato numérico'

                label_resultados = tk.Label(root, text=text)
                label_resultados.update_idletasks()  # Asegura que las medidas se actualicen

                # Calcular la posición para centrar horizontalmente
                x_position = (root.winfo_width() - label_resultados.winfo_reqwidth()) / 2

                # Colocar el label en el centro horizontal
                label_resultados.place(x=x_position, y=150)
                
                # Crear cuadros de entrada para la predicción
                frame_prediccion = tk.Frame(root)
                frame_prediccion.place(x=80, y=500)  # Ajusta la posición según tus necesidades

                tk.Label(frame_prediccion, text="Ingrese los valores para la predicción:").grid(row=0, column=0, columnspan=2)

                entradas_prediccion = []
                for i, col in enumerate(columnas_x_seleccionadas):
                   tk.Label(frame_prediccion, text=f"{col}:").grid(row=i + 1, column=0)
                   valor_var = tk.DoubleVar()
                   entry_valor = tk.Entry(frame_prediccion, textvariable=valor_var)
                   entry_valor.grid(row=i + 1, column=1)
                   entradas_prediccion.append(valor_var)

                # Botón para realizar la predicción
                tk.Button(frame_prediccion, text='Realizar Predicción', command=realizar_prediccion).grid(row=len(columnas_x_seleccionadas) + 1, column=0, columnspan=2, pady=10)
                
def realizar_prediccion():
    global modelo_resultado, root, entradas_prediccion
    

    # Obtener las columnas seleccionadas
    columnas_x_seleccionadas = [col for col, var in colx_vars if var.get()]

    # Mostrar las variables X seleccionadas
    variables_x_seleccionadas_label = tk.Label(root, text=f"Variables X seleccionadas: {', '.join(columnas_x_seleccionadas)}")
    variables_x_seleccionadas_label.place(x=400, y=450)

    # Obtener los valores para la predicción desde las entradas del usuario
    valores_prediccion = [entry.get() for entry in entradas_prediccion]
    

    # Convertir los valores a números
    try:
        valores_prediccion = [float(valor) for valor in valores_prediccion]
    except ValueError:
        # Manejar errores de conversión
        tk.messagebox.showerror("Error", "Ingrese valores numéricos para la predicción.")
        return
    
    datos_predicc = dict(zip(columnas_x_seleccionadas, valores_prediccion))

    # Guardar los datos de predicción en una lista (o cualquier otra estructura de datos que prefieras)
    # En este ejemplo, se utiliza una lista para almacenar varios conjuntos de datos de predicción
    datos_prediccion.append(datos_predicc)
    
    # Realizar la predicción utilizando la función independiente
    predicciones = predecir_nuevos_valores(modelo_resultado, datos_prediccion)

    if predicciones is not None:
        # Mostrar las predicciones
        predicciones_label = tk.Label(root, text=f"Predicciones: {predicciones}")
        predicciones_label.place(x=200, y=480)


def on_label_configure(label):
    label.update_idletasks()
    label.configure(scrollregion=label.bbox("all"))

def grafica_modelo():
    global datos, canvas, label_grafica
    if datos is not None:
        # Destruye la gráfica anterior si existe
        if canvas:
            canvas.get_tk_widget().destroy()
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
            if len(columnas_x_seleccionadas) < 3:
                if len(columnas_x_seleccionadas) == 1:
                    # Crea la gráfica de regresión lineal
                    plt.figure(figsize=(6, 3))
                    plt.scatter(x_test.iloc[:, 0], y_test, color='black')  # Solo se muestra la primera columna X para la gráfica
                    plt.plot(x_test.iloc[:, 0], y_pred, color='blue', linewidth=3)
                    plt.title('Regresión Lineal')
                    plt.xlabel(", ".join(columnas_x_seleccionadas))
                    plt.ylabel(columna_y_seleccionada)
                else:
                    fig = plt.figure(figsize=(6, 3))
                    ax = fig.add_subplot(111, projection='3d')

                    # Scatter plot en 3D
                    ax.scatter(x_test[columnas_x_seleccionadas[0]], x_test[columnas_x_seleccionadas[1]], y_test, color='black')

                    # Plot del plano de regresión en 3D
                    x_range = np.linspace(min(x_test[columnas_x_seleccionadas[0]]), max(x_test[columnas_x_seleccionadas[0]]), 100)
                    y_range = np.linspace(min(x_test[columnas_x_seleccionadas[1]]), max(x_test[columnas_x_seleccionadas[1]]), 100)
                    X, Y = np.meshgrid(x_range, y_range)
                    Z = modelo.coef_[0] * X + modelo.coef_[1] * Y + modelo.intercept_
                    ax.plot_surface(X, Y, Z, alpha=0.5, color='blue')

                    # Configuración de etiquetas y título
                    ax.set_xlabel(columnas_x_seleccionadas[0])
                    ax.set_ylabel(columnas_x_seleccionadas[1])
                    ax.set_zlabel(columna_y_seleccionada)
                    ax.set_title('Regresión Lineal en 3D')
                # Integra la gráfica en la ventana principal
                canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
                canvas.draw()
                canvas.get_tk_widget().place(x=80, y=500)  # Ajusta el valor de padx según tus necesidades
            else:
                text = 'Gráfica no disponible para tantas variables'

                label_grafica = tk.Label(root, text=text)
                label_grafica.update_idletasks()  # Asegura que las medidas se actualicen

                # Calcular la posición para centrar horizontalmente
                x_position = (root.winfo_width() - label_grafica.winfo_reqwidth()) / 2

                # Colocar el label en el centro horizontal
                label_grafica.place(x=x_position, y=500)

def cargar_modelo():
    global modelo_g, ruta_modelo
    limpiar_interfaz()
    # Abrir el cuadro de diálogo para seleccionar un archivo
    ruta_modelo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # Verificar si se ha seleccionado un modelo
    if not ruta_modelo:
        return None

    try:
        with open(ruta_modelo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            
        # Parsear la información del modelo desde el archivo
        dos_puntos = []
        for i in lineas:
            dos_puntos.append(i.find(':'))
        nombre = lineas[0][dos_puntos[0] + 2 : -1]
        descripcion = lineas[1][dos_puntos[1] + 2 : -1]
        parametros_ajuste = lineas[2][dos_puntos[2] + 2 : -1]
        parametros_ajuste = [float(x) for x in parametros_ajuste.strip('[]').split(',')]
        cols_x_dict = ast.literal_eval(lineas[3][dos_puntos[3] + 2 : -1])
        coly = lineas[4][dos_puntos[4] + 2 : -1]
        const = float(lineas[5][dos_puntos[5] + 2 : -1])

        # Create an instance of the Modelo class
        modelo_g = Modelo(nombre, descripcion, parametros_ajuste, cols_x_dict, coly, const)
        # Mostrar la interfaz gráfica para modelos
        mostrar_interfaz_grafica()
        creador_de_modelo('si')

    except Exception as e:
        print(f"Error al cargar el modelo desde {ruta_modelo}: {e}")



# Configuración de la ventana principal
root = tk.Tk()

screen_height = root.winfo_screenheight()

# Define la posición x en 750
x_position = 750

# Calcula la posición y centrada verticalmente
# Configura la posición de la ventana
root.geometry(f"750x{screen_height}+{x_position}+0")

root.title('Aplicación de Regresión Lineal')
root.resizable(width=False, height=False)

ruta_archivo = tk.StringVar()
ruta_label = tk.Label(root, text="Ruta del archivo:")
ruta_label.place(x=10, y=10)
ruta_entry = tk.Entry(root, textvariable=ruta_archivo, state="readonly", width=40)
ruta_entry.place(x=150, y=10)

examinar_button = tk.Button(root, text='Examinar', command=lambda: cargar_y_visualizar_datos())
examinar_button.place(x=450, y=5)

# Crear el botón "Cargar Modelo"
cargar_boton = tk.Button(root, text='Cargar Modelo', command=lambda: cargar_modelo())
cargar_boton.place(x=550, y=5)

button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=3, pady=10)

# Botón "Hacer Regresión"
cargar_regresion = tk.Button(root, text='Hacer Regresión', command=creador_de_modelo)
cargar_regresion.grid(row=7, column=0, columnspan=1, pady=10, sticky="nsew")
cargar_regresion.grid_remove()

# Crear el botón "Guardar Modelo"
guardar_boton = tk.Button(root, text='Guardar Modelo', command=obtener_datos_adicionales)
guardar_boton.grid(row=8, column=0, columnspan=1, padx=10, sticky="nsew")
guardar_boton.grid_remove()



root.mainloop()
