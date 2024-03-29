import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

def crear_data_frame_entero(data):
    datos = pd.DataFrame()
    titulos = list(data.columns)
    for i in titulos:
        datos[i] = np.nan_to_num(data[i], nan=0)
    return datos

def calcular_regresion2(datos, columnas_x_seleccionadas, columna_y_seleccionada):
    datos = crear_data_frame_entero(datos)
    X = datos[columnas_x_seleccionadas]
    y = datos[columna_y_seleccionada]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y.values.reshape(-1, 1),
        train_size=0.8,
        random_state=1234,
        shuffle=True
    )

    X_train = sm.add_constant(X_train, prepend=True)
    modelo = sm.OLS(endog=y_train, exog=X_train)
    modelo = modelo.fit()

    print('\n', modelo.rsquared, modelo.condition_number)
    parametros = list(modelo.params)

    cols_x_dict = {}
    modelo_g = [columna_y_seleccionada, cols_x_dict, parametros[0], [modelo.rsquared, modelo.condition_number]]
    for i in range(1, len(parametros)):
        cols_x_dict[columnas_x_seleccionadas[i - 1]] = parametros[i]

    return modelo_g, modelo  # Se agrega el modelo ajustado

def predecir_nuevos_valores(modelo, datos_nuevos):
    # Añadir la constante a los datos nuevos
    datos_nuevos = sm.add_constant(datos_nuevos, prepend=True)
    # Realizar la predicción
    predicciones = modelo.predict(datos_nuevos)
    return predicciones

def escribir_ecuacion2(modelo_datos):
    text = ''
    text += 'Porcentaje explicado:' + str(modelo_datos[3][0]) + ' Error cometido al cuadrado:' + str(
        modelo_datos[3][1]) + '\n'
    text += str(modelo_datos[0]) + ' = '
    list_keys = []
    for i in modelo_datos[1]:
        list_keys.append(i)
        if len(list_keys) == 1:
            text += str(modelo_datos[1][i]) + ' * ' + str(i) + ' '
        else:
            if modelo_datos[1][i] >= 0:
                text += ' + '
            text += str(modelo_datos[1][i]) + ' * ' + str(i)
    if modelo_datos[2] < 0:
        text += str(modelo_datos[2])
    else:
        text += ' + ' + str(modelo_datos[2])
    return text

# Ejemplo de uso
# Supongamos que tienes un DataFrame llamado 'nuevos_datos' con las mismas columnas que se usaron para entrenar el modelo
# Además, asumimos que 'modelo_datos' y 'modelo' son los resultados de la función 'calcular_regresion2'
# 'modelo_datos' contiene la información de la ecuación y 'modelo' contiene el modelo ajustado

variable1 = [1, 7, 3]
variable2 = [4, 5, 6]
nuevos_datos = pd.DataFrame({'Variable1': variable1, 'Variable2': variable2})
print(nuevos_datos)
predicciones = predecir_nuevos_valores(modelo, nuevos_datos)
print(predicciones)
