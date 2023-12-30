import pandas as pd
import numpy as np
import pytest
from clase_modelo import Modelo  # Asegúrate de tener el archivo de clase_modelo.py en tu proyecto
from error_nan import crear_data_frame_entero, calcular_regresion2, escribir_ecuacion2, predecir_nuevos_valores

# Mock data for testing
data = pd.DataFrame({
    'feature1': [1, 2, 3, 4],
    'feature2': [4, 3, 2, 1],
    'target': [10, 20, 30, 40]
})

columnas_x = ['feature1', 'feature2']
columna_y = 'target'

def test_crear_data_frame_entero():
    df = crear_data_frame_entero(data)
    assert not df.isna().any().any()  # No hay NaN en el DataFrame resultante

def test_calcular_regresion2():
    modelo = calcular_regresion2(data, columnas_x, columna_y)
    assert isinstance(modelo, Modelo)  # Verifica que la salida es una instancia de la clase Modelo
    assert modelo.get_nombre() == "nombre_modelo"  # Ajusta según el valor esperado

def test_escribir_ecuacion2():
    modelo = Modelo(nombre="Modelo de prueba", descripcion="Descripción de prueba", parametros_ajuste=[0.5, 100],
                    cols_x_dict={'feature1': 2, 'feature2': 3}, coly='target', const=10)
    ecuacion = escribir_ecuacion2(modelo)
    assert "Porcentaje explicado: 0.5" in ecuacion
    assert "Error cometido: 10.0" in ecuacion

def test_predecir_nuevos_valores():
    modelo = Modelo(nombre="Modelo de prueba", descripcion="Descripción de prueba", parametros_ajuste=[0.5, 100],
                    cols_x_dict={'feature1': 2, 'feature2': 3}, coly='target', const=10)
    nuevos_datos = {'feature1': 5, 'feature2': 6}
    prediccion = predecir_nuevos_valores(modelo, nuevos_datos)
    assert prediccion == 2 * 5 + 3 * 6 + 10  # Ajusta según el valor esperado

# Ejecutar las pruebas con pytest desde la línea de comandos
# Ejemplo: pytest test.py
