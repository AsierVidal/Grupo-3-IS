El proyecto en el que hemos trabajado desde este grupo es un software que nos permite realizar regresiones lineales a partir de un 
archivo de datos .xls, .csv o .db. El código nos presenta una interfaz gráfica, y una vez indicado el archivo de datos a emplear
nos mostrará la gráfica de la regresión y permitirá al usuario hacer una predicción según la ecuación empleada. Otra funcionalidad 
del código es que se permite al usuario guardar y cargar sus propios modelos para hacer las predicciones.

El código creado está implementado en Python 3.8.10, y para ejecutarlo de manera correcta hay que instalar los siguientes paquetes:

-numpy (con el comando pip install numpy)
-pandas (con el comando pip install pandas)
-matplotlib (con el comando pip install matplotlib)
-statsmodels.api (con el comando pip install statsmodels)
-scikit-learn (con el comando pip install -U scikit-learn)
-tkinter (con el comando pip install tk)

Tras abrir los archivos que integran nuestro código, hay que ejecutar el archivo main.py, que integra el resto de módulos que hemos 
creado. Una vez ejecutado se nos presentará la interfaz gráfica y nos mostrará la ruta del archivo que elijamos y dos opciones: 
abrir nuestro propio modelo (si está creado previamente), o abrir un archivo de datos para realizar la regresión.

Si se elige la opción de cargar un archivo de datos se le presentarán al usuario dos filas, una con checkboxes y variables para
escoger las variables x que se utilizarán en la regresión, y otra fila que solo permitirá elegir una variable, la que será la
variable y de la regresión. Una vez elegidas se nos mostrará la ecuación de la regresión y la gráfica (siempre y cuando la gráfica
sea en 2 o 3 dimensiones).

Si se elige la opción de cargar un modelo creado previamente ya se mostrará directamente la información guardada en el mismo. 
Además, se muestra una opción para hacer una predicción en base al modelo cargado, en la que el usuario tendrá que escoger
valores para las columnas x y el programa devolverá el valor para la columna y.
