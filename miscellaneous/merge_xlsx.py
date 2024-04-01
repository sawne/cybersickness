import os
import pandas as pd

def merge_excel(folder_path):
    # Liste pour stocker tous les dataframes
    dfs = []

    # Parcourir tous les fichiers dans le dossier
    for file in os.listdir(folder_path):
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_excel(file_path)
            dfs.append(df)

    # Fusionner tous les dataframes en un seul
    merged_df = pd.concat(dfs, ignore_index=True)

    # Prétraiter les données comme précédemment
    X = merged_df[['compression']].values
    y = merged_df['isSick'].values

    return X, y
