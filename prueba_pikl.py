import pickle

class Modelo:
    def __init__(self, nombre, descripcion, parametros_ajuste, cols_x_dict, coly, const):
        self.nombre = nombre
        self.descripcion = descripcion
        self.parametros_ajuste = parametros_ajuste
        self.cols_x_dict = cols_x_dict
        self.coly = coly
        self.const = const

def guardar_modelo_en_archivo(ruta, modelo):
    try:
        with open(ruta, 'wb') as archivo:
            pickle.dump(modelo, archivo)
        print(f"Modelo guardado correctamente en {ruta}")
    except Exception as e:
        print(f"Error al guardar el modelo en {ruta}: {e}")

# Ejemplo de uso
modelo_ejemplo = Modelo(
    nombre="Modelo de ejemplo",
    descripcion="Este es un modelo de ejemplo",
    parametros_ajuste=[0.5, 1.2, 3.0],
    cols_x_dict={"feature1": 0, "feature2": 1},
    coly="target",
    const=2.5
)

ruta_archivo_modelo = str(input("En que archivo quieres guardar el modelo?"))
guardar_modelo_en_archivo(ruta_archivo_modelo, modelo_ejemplo)

