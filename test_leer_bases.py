"""IMPORTANTE ESTE TEST CREA 3 ARCHIVOS PARA COMPROBAR QUE FUNCIONAN"""


import pandas as pd
import sqlite3
import pytest
from leerbasededatosexcelycsv import read
import os



# Define las rutas de archivo para usar en las pruebas
CSV_FILE = 'ejemplo.csv'
EXCEL_FILE = 'ejemplo.xlsx'
DB_FILE = 'ejemplo.db'

# Crea archivos de ejemplo
def create_csv_file():
    data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE, index=False)

def create_excel_file():
    data = {'Column1': [4, 5, 6], 'Column2': ['X', 'Y', 'Z']}
    df = pd.DataFrame(data)
    df.to_excel(EXCEL_FILE, index=False)

def create_sqlite_file():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE ejemplo (Column1 INT, Column2 TEXT);''')
    data = [(7, 'M'), (8, 'N'), (9, 'O')]
    cursor.executemany('''INSERT INTO ejemplo (Column1, Column2) VALUES (?, ?);''', data)
    connection.commit()
    connection.close()

# Crea archivos antes de ejecutar las pruebas
create_csv_file()
create_excel_file()
create_sqlite_file()

# Pruebas para la función read
def test_read_csv():
    data = read(CSV_FILE)
    assert isinstance(data, pd.DataFrame)

def test_read_excel():
    data = read(EXCEL_FILE)
    assert isinstance(data, pd.DataFrame)

def test_read_sqlite():
    data = read(DB_FILE)
    assert isinstance(data, pd.DataFrame)
