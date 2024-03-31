
from sklearn.tree import DecisionTreeRegressor

from miscellaneous.merge_xlsx import merge_excel
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

folder_path = "../data_compressed/explorer"

X, y = merge_excel(folder_path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)



# Création du modèle d'arbre de décision pour la régression
tree_regressor = DecisionTreeRegressor(random_state=42)
# Entraînement du modèle
tree_regressor.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred = tree_regressor.predict(X_test)

# Calcul de l'erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Trier les données pour la visualisation
sorted_zip = sorted(zip(X_test, y_pred))
X_test, y_pred = zip(*sorted_zip)

# Visualisation des données et de la régression par arbre de décision
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X_test, y_pred, color='red', label='Decision Tree Regression')
plt.title('Decision Tree Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()

# Exportation du modèle d'arbre de décision
joblib.dump(tree_regressor, 'decision_tree_regression_model.pkl')