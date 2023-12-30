import os
import pytest
from clase_modelo import Modelo  # Asegúrate de importar correctamente la clase Modelo y el módulo que contiene tu implementación

@pytest.fixture
def modelo_de_prueba():
    # Puedes crear un objeto Modelo de prueba con valores específicos para tus pruebas
    return Modelo(
        nombre="ModeloPrueba",
        descripcion="Descripción de prueba",
        parametros_ajuste={"param1": 1, "param2": 2},
        cols_x_dict={"col1": "X1", "col2": "X2"},
        coly="Y",
        const=42
    )

def test_guardar_modelo(tmpdir, modelo_de_prueba):
    # tmpdir es una fixture proporcionada por Pytest que representa un directorio temporal

    # Construye el path del archivo de prueba en el directorio temporal
    archivo_prueba = os.path.join(tmpdir, "modelo_prueba.txt")

    # Ejecuta la función que deseas probar
    modelo_de_prueba.guardar_modelo(archivo_prueba)

    # Lee el contenido del archivo para asegurarte de que se haya guardado correctamente
    with open(archivo_prueba, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    # Realiza las afirmaciones correspondientes para verificar el contenido
    assert "Nombre: ModeloPrueba" in contenido
    assert "Descripción: Descripción de prueba" in contenido
    assert "Parámetros de Ajuste: {'param1': 1, 'param2': 2}" in contenido
    assert "Columnas X: {'col1': 'X1', 'col2': 'X2'}" in contenido
    assert "Columna Y: Y" in contenido
    assert "Constante: 42" in contenido

