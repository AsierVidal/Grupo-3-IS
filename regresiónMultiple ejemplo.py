# Importa las bibliotecas necesarias
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Genera datos de ejemplo
np.random.seed(0)
X = 2 * np.random.rand(100, 3)  # Tres características predictoras
y = 4 + np.dot(X, np.array([3, 1.5, -0.5])) + np.random.randn(100)  # Relación lineal con ruido

# Divide los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crea un modelo de regresión lineal
modelo_regresion = LinearRegression()

# Entrena el modelo con los datos de entrenamiento
modelo_regresion.fit(X_train, y_train)

# Realiza predicciones en el conjunto de prueba
y_pred = modelo_regresion.predict(X_test)

# Evalúa el rendimiento del modelo
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Visualiza los coeficientes del modelo
print('Coeficientes:', modelo_regresion.coef_)
print('Intercepto:', modelo_regresion.intercept_)

# Visualiza la regresión en 3D (para tres características)
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Puntos de datos
ax.scatter(X_test[:, 0], X_test[:, 1], y_test, color='red', marker='o', label='Datos reales')

# Superficie de regresión
x0_range = np.linspace(min(X_test[:, 0]), max(X_test[:, 0]), 100)
x1_range = np.linspace(min(X_test[:, 1]), max(X_test[:, 1]), 100)
x0, x1 = np.meshgrid(x0_range, x1_range)
y_pred_surface = modelo_regresion.predict(np.c_[x0.ravel(), x1.ravel(), np.zeros_like(x0.ravel())])
y_pred_surface = y_pred_surface.reshape(x0.shape)
ax.plot_surface(x0, x1, y_pred_surface, color='blue', alpha=0.5, label='Regresión lineal')

# Etiquetas
ax.set_xlabel('Característica 1')
ax.set_ylabel('Característica 2')
ax.set_zlabel('Variable de respuesta')

# Leyenda
ax.legend()

plt.show()
