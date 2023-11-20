# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:05:05 2023

@author: USUARIO
"""

import pandas as pd
import sqlite3

def read(archivo):
    archivo = archivo.lower()
    if archivo.endswith(".csv"):
        data = pd.read_csv(archivo)
    elif archivo.endswith(".xls") or archivo.endswith(".xlsx"):
        data = pd.read_excel(archivo)
    elif archivo.endswith(".db"):
        connection = sqlite3.connect(archivo)
        cursor = connection.cursor()

        # Obtén la lista de todas las tablas en la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        if not tables:
            print("La base de datos no contiene ninguna tabla.")
            data = read(archivo)
        else:
            table_name = tables[0]
            print(f"Cargando datos de la tabla: {table_name}")
            data = pd.read_sql(f"SELECT * FROM {table_name}", connection)
            
            
        connection.close()
    else:
        archivo = input(f"{archivo} no es válido. Introduce un archivo CSV, Excel o una base de datos SQLite: ")
        data = read(archivo)

    return data

archivo = input('Introduce el archivo que deseas leer: ')
data = read(archivo)
print(data)