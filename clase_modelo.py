import json

class Modelo():
    def __init__(self, nombre, descripcion, parametros_ajuste, cols_x_dict, coly, const):
        self.nombre = nombre
        self.descripcion = descripcion
        self.parametros_ajuste = parametros_ajuste
        self.cols_x_dict = cols_x_dict
        self.coly = coly
        self.const = const
    
    def guardar_modelo(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'w') as archivo:
                modelo_dict = {
                    "nombre": self.nombre,
                    "descripcion": self.descripcion,
                    "parametros_ajuste": self.parametros_ajuste,
                    "cols_x_dict": self.cols_x_dict,
                    "coly": self.coly,
                    "const": self.const
                }
                json.dump(modelo_dict, archivo, indent=4)
                print(f"Modelo guardado correctamente en {ruta_archivo}")
        except Exception as e:
            print(f"Error al guardar el modelo en {ruta_archivo}: {e}")
            
def guardar_texto_en_archivo(ruta, texto):
    try:
        with open(ruta, 'w') as archivo:
            archivo.write(texto)
        print(f"Texto guardado correctamente en {ruta}")
    except Exception as e:
        print(f"Error al guardar el texto en {ruta}: {e}")