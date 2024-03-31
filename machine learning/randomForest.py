from sklearn.ensemble import RandomForestRegressor
from miscellaneous.merge_xlsx import merge_excel
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

folder_path = "../data_compressed/explorer"

X, y = merge_excel(folder_path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Création du modèle Random Forest pour la régression
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# Entraînement du modèle
rf_regressor.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred = rf_regressor.predict(X_test)

# Calcul de l'erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Trier les données pour la visualisation
sorted_zip = sorted(zip(X_test, y_pred))
X_test, y_pred = zip(*sorted_zip)

# Visualisation des données et de la régression par Random Forest
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X_test, y_pred, color='red', label='Random Forest Regression')
plt.title('Random Forest Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()

# Exportation du modèle Random Forest
joblib.dump(rf_regressor, 'random_forest_regression_model.pkl')
