
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
    # Aplicar la función para manejar NaN
    datos = crear_data_frame_entero(datos)

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
    modelo = sm.OLS(endog=y_train, exog=X_train)
    modelo = modelo.fit()

    print('\n', modelo.rsquared, modelo.condition_number)
    parametros = list(modelo.params)

    cols_x_dict = {}
    modelo_g = [columna_y_seleccionada, cols_x_dict, parametros[0], [modelo.rsquared, modelo.condition_number]]
    for i in range(1, len(parametros)):
        cols_x_dict[columnas_x_seleccionadas[i - 1]] = parametros[i]

    return modelo_g