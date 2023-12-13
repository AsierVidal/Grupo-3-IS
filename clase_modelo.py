class Modelo():
    def __init__(self, nombre, descripcion, parametros_ajuste, cols_x_dict, coly, const):
        self.nombre = nombre
        self.descripcion = descripcion
        self.parametros_ajuste = parametros_ajuste
        self.cols_x_dict = cols_x_dict
        self.coly = coly
        self.const = const
    
    def guardar_modelo(self):
        archivo = open("mi_archivo.txt", "w", encoding="utf-8") #abre el archivo

        archivo.write(self.nombre,",") #escribe texto en el archivo

        archivo.close() # cierra el archivo




modelo = Modelo('m1','d1',[0.7,7],{'d1':7,'d2':8},'coly',3)


"""archivo = open("mi_archivo.txt", "w", encoding="utf-8") #abre el archivo

archivo.write(self.nombre,",",self.descripcion,",",) #escribe texto en el archivo

archivo.close() # cierra el archivo"""

def guardar_texto_en_archivo(ruta, texto):
    try:
        with open(ruta, 'w') as archivo:
            archivo.write(texto)
        print(f"Texto guardado correctamente en {ruta}")
    except Exception as e:
        print(f"Error al guardar el texto en {ruta}: {e}")


