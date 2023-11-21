import tkinter as tk
from tkinter import filedialog, ttk,simpledialog,Toplevel,messagebox
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from error_nan import crear_data_frame_entero,calcular_regresion2
from leerbasededatosexcelycsv import read
import json
#from guardar_modelo import guardar_modelo, mostrar_detalles_modelo  


 


# Declara datos como variable global
datos = None

# Variables para almacenar las columnas X e Y
colx_vars = []
coly_var = None
modelos_guardados = {}
ruta_archivo = None


def cargar_y_visualizar_datos():
    global datos, ruta_archivo
    archivo = filedialog.askopenfilename()
    if archivo:
        ruta_archivo.set(archivo)  # Actualiza la variable ruta_archivo
        datos = read(archivo)
        # Mostrar las columnas en la consola
        print("Columnas disponibles:")
        print(datos.columns)

        # Actualiza el widget Text con las primeras filas del DataFrame
        text_widget.delete(1.0, tk.END)  # Borra el contenido actual
        text_widget.insert(tk.END, datos.to_string(index=False))

        # Limpiar las columnas anteriores
        for widget in frame_x.winfo_children():
            widget.destroy()
        for widget in frame_y.winfo_children():
            widget.destroy()

        # Crear checkboxes para seleccionar múltiples columnas X
        global colx_vars, coly_var
        coly_var = tk.StringVar()
        coly_var.set(datos.columns[0])  # Establecer el valor predeterminado como la primera columna

        # Contenedor para las columnas X
        label_x = tk.Label(frame_x, text="COLUMNAS X")
        label_x.grid(row=0, column=0)

        for i, col in enumerate(datos.columns):
            var = tk.BooleanVar()
            colx_vars.append((col, var))
            checkbox_x = tk.Checkbutton(frame_x, text=col, variable=var)
            checkbox_x.grid(row=i + 1, column=0)

        # Contenedor para la columna Y
        label_y = tk.Label(frame_y, text="COLUMNA Y")
        label_y.grid(row=0, column=0)

        for i, col in enumerate(datos.columns):
            radio_button_y = tk.Radiobutton(frame_y, text=col, variable=coly_var, value=col)
            radio_button_y.grid(row=i + 1, column=0)


def crear_modelo_regresion():
    cargar_y_visualizar_datos()

def guardar_modelo():
    global modelos_guardados, nombre_modelo, modelo_g

    if nombre_modelo and modelo_g:
        # Guarda el modelo en el diccionario
        modelos_guardados[nombre_modelo] = modelo_g

        # Guarda el diccionario en un archivo JSON
        with open("modelos_guardados.json", "w") as f:
            json.dump(modelos_guardados, f)
        print("Modelo guardado exitosamente.")
    else:
        print("No hay modelo para guardar.")

def mostrar_detalles_modelo(nombre_modelo):
    global modelos_guardados
    modelo_g = modelos_guardados.get(nombre_modelo)

    if modelo_g:
        ventana_detalles = Toplevel(root)
        ventana_detalles.title(f"Detalles del Modelo: {nombre_modelo}")

        # Mostrar detalles en la nueva ventana
        label_nombre = tk.Label(ventana_detalles, text=f"Nombre del Modelo: {nombre_modelo}")
        label_nombre.pack()

        label_columna_y = tk.Label(ventana_detalles, text=f"Columna Y seleccionada: {modelo_g[1]}")
        label_columna_y.pack()

        label_columnas_x = tk.Label(ventana_detalles, text=f"Columnas X seleccionadas: {', '.join(modelo_g[2])}")
        label_columnas_x.pack()

        label_r_squared = tk.Label(ventana_detalles, text=f"R^2: {modelo_g[4][0]}")
        label_r_squared.pack()

        label_condition_number = tk.Label(ventana_detalles, text=f"Condición: {modelo_g[4][1]}")
        label_condition_number.pack()
    else:
        print(f"No se encontró el modelo con el nombre: {nombre_modelo}")


def creador_de_modelo():
    global datos, colx_vars, coly_var, root, modelos_guardados, nombre_modelo, modelo_g

    # Obtener las columnas seleccionadas
    columnas_x_seleccionadas = [col for col, var in colx_vars if var.get()]
    columna_y_seleccionada = coly_var.get()

    # Mostrar las columnas X e Y en la consola
    print(f"Se han seleccionado las columnas X: {columnas_x_seleccionadas}")
    print(f"Se ha seleccionado la columna Y: {columna_y_seleccionada}")

    # Solicitar al usuario que ingrese un nombre para el modelo desde la interfaz
    nombre_modelo = simpledialog.askstring("Nombre del Modelo", "Ingrese un nombre para el modelo:")

    if nombre_modelo and columnas_x_seleccionadas and columna_y_seleccionada:
        # Aquí puedes realizar las operaciones para calcular la regresión utilizando las columnas seleccionadas
        modelo_g = calcular_regresion2(datos, columnas_x_seleccionadas, columna_y_seleccionada, nombre_modelo)

        # Mostrar la información en la interfaz gráfica
        label_columnas_x = tk.Label(root, text=f"Columnas X seleccionadas: {', '.join(columnas_x_seleccionadas)}")
        label_columnas_x.grid(row=4, column=0, columnspan=3, pady=10)

        label_columna_y = tk.Label(root, text=f"Columna Y seleccionada: {columna_y_seleccionada}")
        label_columna_y.grid(row=5, column=0, columnspan=3, pady=10)

        label_resultados = tk.Label(root, text=f"R^2: {modelo_g[4][0]}, Condición: {modelo_g[4][1]}")
        label_resultados.grid(row=6, column=0, columnspan=3, pady=10)

        # Botones en una fila superior
        guardar_boton = tk.Button(button_frame, text='Guardar Modelo', command=guardar_modelo)
        guardar_boton.grid(row=5, column=0, padx=5)

        print("Modelo creado exitosamente.")
    else:
        print("Selecciona al menos una columna X y una columna Y antes de calcular la regresión.")

  
def actualizar_interfaz(modelo_g):
    # Limpiar la información anterior
    for widget in frame_info_modelo.winfo_children():
        widget.destroy()

    # Mostrar la información actualizada en la interfaz gráfica
    label_nombre = tk.Label(frame_info_modelo, text=f"Nombre del Modelo: {modelo_g[0]}")
    label_nombre.grid(row=0, column=0, pady=5)

    label_columnas_x = tk.Label(frame_info_modelo, text=f"Columnas X seleccionadas: {', '.join(modelo_g[2])}")
    label_columnas_x.grid(row=1, column=0, pady=5)

    label_columna_y = tk.Label(frame_info_modelo, text=f"Columna Y seleccionada: {modelo_g[1]}")
    label_columna_y.grid(row=2, column=0, pady=5)

    label_r_squared = tk.Label(frame_info_modelo, text=f"R^2: {modelo_g[4][0]}")
    label_r_squared.grid(row=3, column=0, pady=5)

    label_condition_number = tk.Label(frame_info_modelo, text=f"Condición: {modelo_g[4][1]}")
    label_condition_number.grid(row=4, column=0, pady=5)

def mostrar_nombres_modelos():
    global modelos_guardados

    if modelos_guardados:
        # Ocultar la ventana principal
        root.withdraw()

        # Crear una nueva ventana principal para mostrar los modelos guardados
        ventana_modelos = Toplevel(root)
        ventana_modelos.title("Modelos Guardados")

        # Mostrar nombres de los modelos con botones para ver detalles
        for nombre_modelo in modelos_guardados:
            boton_modelo = tk.Button(ventana_modelos, text=nombre_modelo, command=lambda n=nombre_modelo: mostrar_detalles_modelo_seleccionado(n))
            boton_modelo.pack()

        # Botón de regreso
        boton_atras = tk.Button(ventana_modelos, text='Atrás', command=lambda: [ventana_modelos.destroy(), root.deiconify()])
        boton_atras.pack()

    else:
        # Mensaje si no hay modelos guardados
        messagebox.showinfo("Modelos Guardados", "No hay modelos guardados.")

def cargar_modelo_seleccionado(nombre_modelo):
    global modelos_guardados

    modelo_g = modelos_guardados.get(nombre_modelo)

    if modelo_g:
        # Mostrar detalles del modelo seleccionado
        actualizar_interfaz(modelo_g)

def mostrar_detalles_modelo_seleccionado(nombre_modelo):
    global modelos_guardados

    modelo_g = modelos_guardados.get(nombre_modelo)

    if modelo_g:
        ventana_detalles = Toplevel(root)
        ventana_detalles.title(f"Detalles del Modelo: {nombre_modelo}")

        # Mostrar detalles en la nueva ventana
        label_nombre = tk.Label(ventana_detalles, text=f"Nombre del Modelo: {modelo_g[0]}")
        label_nombre.pack()

        label_columna_y = tk.Label(ventana_detalles, text=f"Columna Y seleccionada: {modelo_g[1]}")
        label_columna_y.pack()

        label_columnas_x = tk.Label(ventana_detalles, text=f"Columnas X seleccionadas: {', '.join(modelo_g[2])}")
        label_columnas_x.pack()

        label_r_squared = tk.Label(ventana_detalles, text=f"R^2: {modelo_g[4][0]}")
        label_r_squared.pack()

        label_condition_number = tk.Label(ventana_detalles, text=f"Condición: {modelo_g[4][1]}")
        label_condition_number.pack()

 
        
  

def cargar_modelo():
    global datos
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
            plt.scatter(x_test.iloc[:, 0], y_test, color='black')  # Solo se muestra la primera columna X para la gráfica
            plt.plot(x_test.iloc[:, 0], y_pred, color='blue', linewidth=3)
            plt.title('Regresión Lineal')
            plt.xlabel(", ".join(columnas_x_seleccionadas))
            plt.ylabel(columna_y_seleccionada)

            # Integra la gráfica en la ventana principal
            canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=4, rowspan=3)

            print("Modelo de regresión lineal cargado y visualizado.")
        else:
            print("Selecciona al menos una columna X y una columna Y antes de cargar el modelo.")
    else:
        print("Carga los datos antes de intentar cargar un modelo.")


def hacer_prediccion():
    pass


# Configuración de la ventana principal
root = tk.Tk()
root.geometry("1200x950")
root.title('Aplicación de Regresión Lineal')
root.resizable(width=True, height=True)

 

# Etiqueta, entrada y botón para la ruta del archivo
ruta_archivo = tk.StringVar()
ruta_label = tk.Label(root, text="Ruta del archivo:")
ruta_label.grid(row=0, column=0, pady=10, padx=10)

ruta_entry = tk.Entry(root, textvariable=ruta_archivo, state="readonly", width=40)
ruta_entry.grid(row=0, column=1, pady=5)

examinar_button = tk.Button(root, text='Examinar', command=lambda: cargar_y_visualizar_datos())
examinar_button.grid(row=0, column=2, padx=5, pady=10)

# Widget Text para mostrar los datos
text_widget = tk.Text(root, height=10, width=150, wrap="none")
text_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Contenedor para las columnas X
frame_x = tk.Frame(root)
frame_x.grid(row=2, column=0, padx=10, pady=10)

# Contenedor para la columna Y
frame_y = tk.Frame(root)
frame_y.grid(row=2, column=1, padx=10, pady=10)

# Cuadro de botones para operaciones
button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=3, pady=10)



cargar_boton = tk.Button(button_frame, text='Cargar Modelo', command=cargar_modelo)
cargar_boton.grid(row=1, column=1, padx=10)

cargar_regresion = tk.Button(button_frame, text='Hacer Regresión', command=creador_de_modelo)
cargar_regresion.grid(row=1, column=2, padx=10)

boton_prediccion = tk.Button(button_frame, text='Hacer Predicción', command=hacer_prediccion)
boton_prediccion.grid(row=1, column=3, padx=10)

# Botón para ver modelos guardados
ver_modelos_boton = tk.Button(button_frame, text='Ver Modelos Guardados', command=mostrar_nombres_modelos)
ver_modelos_boton.grid(row=1, column=4, padx=10)



root.mainloop()