import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from clase_modelo import Modelo  # Importar la clase Modelo


# Función para crear un DataFrame y manejar NaN
def crear_data_frame_entero(data):
    datos = pd.DataFrame()
    titulos = list(data.columns)
    for i in titulos:
        datos[i] = np.nan_to_num(data[i], nan=0)
    return datos


# Función para realizar regresión lineal
def calcular_regresion2(datos, columnas_x_seleccionadas, columna_y_seleccionada):
    # Aplicar la función para manejar NaN
    datos = crear_data_frame_entero(datos)

    # Resto del código sigue igual...
    X = datos[columnas_x_seleccionadas]
    y = datos[columna_y_seleccionada]

    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y.values.reshape(-1, 1),
        train_size=0.8,
        random_state=1234,
        shuffle=True
    )

    # Creación del modelo utilizando matrices como en scikit-learn
    X_train = sm.add_constant(X_train, prepend=True)
    modelo_sm = sm.OLS(endog=y_train, exog=X_train)
    modelo_resultado = modelo_sm.fit()
    parametros = list(modelo_resultado.params)

    colsx = {}
    for i in range(1, len(parametros)):
        colsx[columnas_x_seleccionadas[i - 1]] = parametros[i]

    # Crear una instancia de la clase Modelo
    modelo_g = Modelo(
        nombre="nombre_modelo",  # Reemplaza con el nombre que desees
        descripcion="descripcion_modelo",  # Reemplaza con la descripción que desees
        # Cambiado a modelo_resultado.params[0]
        parametros_ajuste=[modelo_resultado.rsquared,
                           modelo_resultado.condition_number],
        cols_x_dict=colsx,
        coly=columna_y_seleccionada,
        const=parametros[0]  # Puedes ajustar esto según tus necesidades
    )
    return modelo_g, modelo_resultado


# Función para escribir la ecuación de regresión
def escribir_ecuacion2(modelo_datos):
    # Agregamos verificación para asegurar que modelo_datos es instancia de la clase Modelo
    if isinstance(modelo_datos, Modelo):
        text_leyenda = ''
        text_leyenda += 'Porcentaje explicado: ' + \
            str(round(modelo_datos.parametros_ajuste[0], 3)) + '    Error cometido: ' + str(
                round((modelo_datos.parametros_ajuste[1])**(1/2), 3))
        text_ecuacion_enter = 0
        text_ecuacion = str(modelo_datos.coly) + ' = '
        list_keys = []
        for i in modelo_datos.cols_x_dict:
            # Miramos si nos vamos a pasar del ancho máximo para que se pueda ver bien
            if len(text_ecuacion) - text_ecuacion_enter > 70:
                text_ecuacion += '\n'
                text_ecuacion_enter = len(text_ecuacion) - 1
            list_keys.append(i)
            if len(list_keys) == 1:
                text_ecuacion += str(
                    round(modelo_datos.cols_x_dict[i], 3)) + ' * ' + str(i) + ' '
            else:
                if modelo_datos.cols_x_dict[i] >= 0:
                    text_ecuacion += '+ '
                text_ecuacion += str(
                    round(modelo_datos.cols_x_dict[i], 3)) + ' * ' + str(i) + ' '
        if len(text_ecuacion) - text_ecuacion_enter > 70:
            text_ecuacion += '\n'
            text_ecuacion_enter = len(text_ecuacion) - 1
        if modelo_datos.const < 0:
            text_ecuacion += str(round(modelo_datos.const, 3))
        else:
            text_ecuacion += '+ ' + str(round(modelo_datos.const, 3))
        text = text_leyenda + '\n' + text_ecuacion
    else:
        text = "Modelo de datos no válido."
    return text


# Función para predecir nuevos valores
def predecir_nuevos_valores(modelo, nuevos_datos):
    predicciones = 0
    for i in nuevos_datos.keys():
        # Multiplicamos los valores proporcionados por su respectivo coeficiente
        predicciones += nuevos_datos[i] * modelo.get_cols_x_dict()[i]
    predicciones += modelo.get_const()
    return predicciones
