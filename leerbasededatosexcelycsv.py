import pandas as pd
import sqlite3


def read(archivo):
    extension = archivo.lower()
    # Para saber que extensión tiene el archivo y entonces decidir que función realizar
    if extension.endswith(".csv"):
        data = pd.read_csv(archivo)
    elif extension.endswith((".xls", ".xlsx")):
        data = pd.read_excel(archivo)
    elif extension.endswith(".db"):
        try:
            connection = sqlite3.connect(archivo)
            cursor = connection.cursor()

            # Obtén la lista de todas las tablas en la base de datos
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]

            if not tables:
                raise ValueError(
                    f"No hay tablas en la base de datos: {archivo}")

            table_name = tables[0]
            data = pd.read_sql(f"SELECT * FROM {table_name}", connection)

        finally:
            connection.close()
    else:
        raise ValueError(
            f"{archivo} no es válido. Introduce un archivo CSV, Excel o una base de datos SQLite.")
    return data
