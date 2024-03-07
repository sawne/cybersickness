from sklearn.preprocessing import PolynomialFeatures
from merge_xlsx import merge_excel
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

folder_path = "../data/tmp"

X, y = merge_excel(folder_path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# Création des caractéristiques polynomiales
degree = 2  # Degré du polynôme
poly_features = PolynomialFeatures(degree=degree)
X_train_poly = poly_features.fit_transform(X_train)
X_test_poly = poly_features.transform(X_test)

# Création du modèle de régression linéaire
model = LinearRegression()

# Entraînement du modèle
model.fit(X_train_poly, y_train)

# Prédiction sur l'ensemble de test
y_pred = model.predict(X_test_poly)

# Calcul de l'erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Trier les données pour la visualisation
sorted_zip = sorted(zip(X_test, y_pred))
X_test, y_pred = zip(*sorted_zip)

# Visualisation des données et de la régression polynomiale
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X_test, y_pred, color='red', label=f'Polynomial Regression (degree={degree})')
plt.title('Polynomial Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()