from sklearn.linear_model import BayesianRidge
from miscellaneous.merge_xlsx import merge_excel
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

folder_path = "../data/tmp"

X, y = merge_excel(folder_path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Création du modèle de régression bayésienne
bayesian_regressor = BayesianRidge()

# Entraînement du modèle
bayesian_regressor.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred, y_std = bayesian_regressor.predict(X_test, return_std=True)

# Calcul de l'erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Trier les données pour la visualisation
sorted_zip = sorted(zip(X_test, y_pred))
X_test, y_pred = zip(*sorted_zip)

# Visualisation des données et de la régression bayésienne
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X_test, y_pred, color='red', label='Bayesian Regression')
plt.fill_between(X_test, y_pred - y_std, y_pred + y_std, color='orange', alpha=0.3)
plt.title('Bayesian Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()
