from miscellaneous.merge_xlsx import merge_excel
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

folder_path = "../data/tmp"

X, y = merge_excel(folder_path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Création du modèle de régression Ridge
alpha = 0.1  # Paramètre de régularisation, à ajuster selon les besoins
ridge = Ridge(alpha=alpha)

# Entraînement du modèle
ridge.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred = ridge.predict(X_test)

# Calcul de l'erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Visualisation des données et de la régression Ridge
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X_test, y_pred, color='red', label='Ridge Regression')
plt.title('Ridge Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()
