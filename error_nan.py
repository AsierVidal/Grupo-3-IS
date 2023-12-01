
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm


        
def crear_data_frame_entero(data):
    datos = pd.DataFrame()
    titulos = list(data.columns)
    for i in titulos:
        datos[i] = np.nan_to_num(data[i], nan=0)
    return (datos)


def calcular_regresion2(datos, columnas_x_seleccionadas, columna_y_seleccionada):
    # Resto del código sigue igual...
    X = datos[columnas_x_seleccionadas]
    y = datos[columna_y_seleccionada]

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

    print('\n', modelo_resultado.rsquared, modelo_resultado.condition_number)
    parametros = list(modelo_resultado.params)

    cols_x_dict = {}
    for i in range(1, len(parametros)):
        cols_x_dict[columnas_x_seleccionadas[i - 1]] = parametros[i]

    # Crear una instancia de la clase Modelo
    modelo_g = Modelo(
        nombre="nombre_modelo",  # Reemplaza con el nombre que desees
        descripcion="descripcion_modelo",  # Reemplaza con la descripción que desees
        parametros_ajuste=parametros[0],
        cols_x_dict=cols_x_dict,
        coly=columna_y_seleccionada,
        const=modelo_resultado.rsquared  # Puedes ajustar esto según tus necesidades
    )

    return modelo_g