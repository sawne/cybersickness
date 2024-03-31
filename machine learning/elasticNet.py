from sklearn.linear_model import ElasticNet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from miscellaneous.merge_xlsx import merge_excel
import joblib

folder_path = "../data_compressed/explorer"

X, y = merge_excel(folder_path)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Création du modèle de régression ElasticNet
alpha = 0.1  # Paramètre de régularisation L1 (Lasso)
l1_ratio = 0.5  # Ratio de mélange de la régularisation L1 (Lasso) et L2 (Ridge)
elastic_net = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)

# Entraînement du modèle
elastic_net.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred = elastic_net.predict(X_test)

# Calcul de l'erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Visualisation des données et de la régression ElasticNet
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X_test, y_pred, color='red', label='ElasticNet Regression')
plt.title('ElasticNet Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()

# Exportation du modèle ElasticNet
joblib.dump(elastic_net, 'elastic_net_regression_model.pkl')
