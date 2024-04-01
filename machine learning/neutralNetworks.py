import joblib
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os
import openpyxl
import numpy as np

# Chemin vers le dossier contenant les fichiers Excel
folder_path = "../data_compressed/explorer"

# Liste pour stocker les séquences temporelles pour chaque participant
participant_sequences = []

# Parcours des fichiers dans le dossier
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
        # Charger le fichier Excel
        wb = openpyxl.load_workbook(os.path.join(folder_path, filename))
        ws = wb.active

        # Extraire les données de compression et d'état de santé
        sequence = []
        for row in ws.iter_rows(values_only=True):
            # Ignorer la première ligne qui contient les en-têtes
            if row[0] != "compression" and row[1] != "isSick":
                sequence.append((row[0], row[1]))  # Tuple (compression, isSick)

        # Organiser les séquences en tenant compte de la dépendance entre les valeurs isSick
        compressed_data = [data[0] for data in sequence]
        is_sick_data = [0] + [1 if sequence[i + 1][0] > sequence[i][0] else -1 for i in range(len(sequence) - 1)]
        participant_sequences.append((compressed_data, is_sick_data))

# Création des données d'entraînement et de test
X = np.concatenate([np.array(seq[0]).reshape(-1, 1) for seq in participant_sequences])
y = np.concatenate([np.array(seq[1]) for seq in participant_sequences])

print(X, y)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Création du modèle de réseau de neurones pour la régression
mlp_regressor = MLPRegressor(hidden_layer_sizes=(100,), activation='relu', solver='adam', random_state=42)

# Entraînement du modèle
mlp_regressor.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred = mlp_regressor.predict(X_test)

# Calcul de l'erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Visualisation des données et de la régression par réseau de neurones
plt.scatter(X_test, y_test, color='blue', label='Actual Data')
plt.scatter(X_test, y_pred, color='red', label='Predicted Data')
plt.title('Neural Network Regression')
plt.xlabel('Compression')
plt.ylabel('isSick')
plt.legend()
plt.show()

# Exportation du modèle de réseau de neurones
# joblib.dump(mlp_regressor, '../models/neural_network_regression_model.pkl')
