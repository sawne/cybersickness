from miscellaneous.merge_xlsx import merge_excel
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

folder_path = "../data_compressed/explorer"

X, y = merge_excel(folder_path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Création du modèle de régression Lasso
alpha = 0.1  # Paramètre de régularisation, à ajuster selon les besoins
lasso = Lasso(alpha=alpha)

# Entraînement du modèle
lasso.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred = lasso.predict(X_test)

# Calcul de l'erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Visualisation des données et de la régression Lasso
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X_test, y_pred, color='red', label='Lasso Regression')
plt.title('Lasso Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()