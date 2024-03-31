from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from miscellaneous.merge_xlsx import merge_excel
import joblib

folder_path = "../data_compressed/explorer"

X, y = merge_excel(folder_path)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Création du modèle de régression linéaire
regr = LinearRegression()

# Entraînement du modèle
regr.fit(X_train, y_train)

# Prédiction
y_pred = regr.predict(X_test)

# The coefficients
print("Coefficients: \n", regr.coef_)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

# Plot outputs
plt.scatter(X_test, y_test, color="black")
plt.plot(X_test, y_pred, color="blue", linewidth=3)
plt.title('Régression linéaire')
plt.xlabel('X')
plt.ylabel('y')


plt.xticks(())
plt.yticks(())

plt.show()

# Exportation du modèle de régression linéaire
joblib.dump(regr, 'linear_regression_model.pkl')
