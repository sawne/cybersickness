from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import matplotlib.pyplot as plt
from miscellaneous.merge_xlsx import merge_excel

# Charger vos données
folder_path = "../data_compressed/explorer"
X, y = merge_excel(folder_path)

# Diviser les données en ensembles de formation et de test
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
X_test_sorted, y_pred_sorted = zip(*sorted_zip)

# Créer une plage d'indices pour les données de test
indices = range(len(X_test_sorted))

# Visualisation des données et de la régression bayésienne
plt.scatter(indices, y_test, color='blue', label='Actual Data')
plt.plot(indices, y_pred_sorted, color='red', label='Predicted Data')
plt.fill_between(indices, y_pred_sorted - y_std, y_pred_sorted + y_std, color='orange', alpha=0.3)
plt.title('Bayesian Regression')
plt.xlabel('Sample Index')
plt.ylabel('isSick')
plt.legend()
plt.show()


# Exportation du modèle
joblib.dump(bayesian_regressor, '../models/bayesian_regression_model.pkl')
