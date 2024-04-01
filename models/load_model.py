import joblib
import pandas as pd

# Charger les nouvelles données
new_data_path = "../data_compressed/labyrinth/participant_5_conversion.xlsx"
new_data = pd.read_excel(new_data_path)

# Supposons que vos données contiennent deux colonnes nommées 'compression' et 'isSick'
# Vous devez les prétraiter de la même manière que vous avez prétraité vos données d'entraînement
# Assurez-vous de remplacer les valeurs manquantes ou d'appliquer d'autres transformations nécessaires

# Sélectionner les colonnes pertinentes pour la prédiction
X_new = new_data[['compression']]

# Charger le modèle
loaded_model = joblib.load('neural_network_regression_model.pkl')

# Faire des prédictions sur de nouvelles données
predictions = loaded_model.predict(X_new)

# Afficher les prédictions
print(predictions)
