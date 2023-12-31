import tkinter as tk


class Modelo():
    # Inicializa la instancia de la clase Modelo con los parámetros dados.
    def __init__(self, nombre, descripcion, parametros_ajuste, cols_x_dict, coly, const):
        self.nombre = nombre
        self.descripcion = descripcion
        self.parametros_ajuste = parametros_ajuste
        self.cols_x_dict = cols_x_dict
        self.coly = coly
        self.const = const

    # Getters y setters de la clase Modelo
    def set_nombre(self, nuevo_nombre):
        self.nombre = nuevo_nombre

    def get_nombre(self):
        return self.nombre

    def set_descripcion(self, nueva_descripcion):
        self.descripcion = nueva_descripcion

    def get_descripcion(self):
        return self.descripcion

    def set_parametros_ajuste(self, nuevos_parametros_ajuste):
        self.parametros_ajuste = nuevos_parametros_ajuste

    def get_parametros_ajuste(self):
        return self.parametros_ajuste

    def set_cols_x_dict(self, nuevas_cols_x_dict):
        self.cols_x_dict = nuevas_cols_x_dict

    def get_cols_x_dict(self):
        return self.cols_x_dict

    def set_coly(self, nueva_coly):
        self.coly = nueva_coly

    def get_coly(self):
        return self.coly

    def set_const(self, nueva_const):
        self.const = nueva_const

    def get_const(self):
        return self.const

    # Funcion para guardar un modelo
    def guardar_modelo(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                # Escribe la información del modelo en el archivo.
                archivo.write(f"Nombre: {self.nombre}\n")
                archivo.write(f"Descripción: {self.descripcion}\n")
                archivo.write(
                    f"Parámetros de Ajuste: {self.parametros_ajuste}\n")
                archivo.write(f"Columnas X: {self.cols_x_dict}\n")
                archivo.write(f"Columna Y: {self.coly}\n")
                archivo.write(f"Constante: {self.const}\n")

        except PermissionError:
            # Muestra un mensaje de error si hay un problema de permisos.
            tk.messagebox.showerror("Error de permisos",
                                    "No se puede escribir en el archivo.")
        except FileNotFoundError:
            # Muestra un mensaje de error si el archivo no se encuentra.
            tk.messagebox.showerror("Error", "Archivo no encontrado.")
        except IsADirectoryError:
            # Muestra un mensaje de error si la ruta especificada es un directorio.
            tk.messagebox.showerror(
                "Error", "La ruta especificada es un directorio, no un archivo.")
