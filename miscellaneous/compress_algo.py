## Modules
import csv
import math

import plotly.graph_objects as go
import pandas as pd

import openpyxl
from matplotlib import pyplot
from openpyxl.utils import get_column_letter
from datetime import datetime
import os

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

##extraction fichier
csv_file = "../data_collected/labyrinth/participant_11.csv"
# csv_file = "./cyril.csv"

position_data = []
isSick_data = []

# Extract data_collected
with open(csv_file, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    next(csv_reader)  # Ignorer l'en-tête
    for line in csv_reader:
        x = float(line[1])
        y = float(line[2])
        z = float(line[3])
        is_sick = int(line[5])
        position_data.append([x, y, z])     # y = 0 for the labyrinth (unity measurement not always as 0)
        isSick_data.append(is_sick)

# Cut list in sublist of 120 elements, 120 is the number of movements collected for 1 answer of sickness
sublist_length = 120    # We keep it as a variable in case we need to change it

position_data_list = []
isSick_data_list = []

# Divide position data_collected into 120 elements
for i in range(0, len(position_data), sublist_length):
    sublist = position_data[i:i + sublist_length]   # 0:119 - 120:239 - 240:359...
    if len(sublist) == sublist_length:  # if sublist has not 120 elements it's too short to keep it
        position_data_list.append(sublist)

# Divide isSick into 120 elements
for i in range(0, len(isSick_data), sublist_length):
    sublist = isSick_data[i:i + sublist_length]
    if len(sublist) == sublist_length:
        isSick_data_list.append(sublist)

# Keep only 1 example of isSick data_collected
isSick = []
for sublist in isSick_data_list:
    isSick.append(sublist[0])

## definition des variables importantes
# Clean point too close of 0.3 distance
distance_threshold = 0.00000000001

# Try different metrics
radius = 1.5

#n<120 n est le nombre de point d'écart entre chaque prise
n=10

## Fonctions utiles

# Return distance between two points in format [x,y,z]
def distance(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2 + (point_a[2] - point_b[2]) ** 2)


# Create a cylinder between two points
# j = k (start point) and o = i (end point)
def define_cylinder(a, b, c, points_list, k, rad, p):

    eq_cylinder = ((
        ((points_list[p][1] - points_list[k][1]) * c - (points_list[p][2] - points_list[k][2]) * b)**2 +
        ((points_list[p][2] - points_list[k][2]) * a - (points_list[p][0] - points_list[k][0]) * c)**2 +
        ((points_list[p][0] - points_list[k][0]) * b - (points_list[p][1] - points_list[k][1]) * a)**2)) \
                  / (a ** 2 + b ** 2 + c ** 2)

    if eq_cylinder < (rad ** 2):
        return True

    else:
        return False

# Calculate the vector director between two points
def calculate_vector_dir(points_list, i,k):
    vector = (points_list[k][0] - points_list[i][0],
              points_list[k][1] - points_list[i][1],
              points_list[k][2] - points_list[i][2])

    return vector


#petite_liste est un bout des listes de tailles 120
def calcul_general(petite_liste,count_compression,plot_compression_liste):
    compteur=count_compression
    n=len(petite_liste)
    liste=plot_compression_liste

    liste.append(petite_liste[0])

    a, b, c = calculate_vector_dir(petite_liste,0,-1)  # VEC DIR
    # Check if clean_sublist[i - 1] is inside the cylinder
    for p in range(1,len(petite_liste)):
        if define_cylinder(a, b, c, petite_liste, 0, radius, p):
            compteur += 1
        else:
            liste.append(petite_liste[p])
    return (compteur,plot_compression_liste)

## Algo

compression_list=[]
len_of_all_plot_compression_list_percentage=[]
plot_compression_liste=[]

# For each sublist we compress movement player list and calculate the compression ratio
for sublist in position_data_list:
    cleaned_sublist = []  # Sublist without points too close together
    count_compression = 0

    # Clean points too close together
    for i in range(1, 120):
        if distance(sublist[i], sublist[i - 1]) < distance_threshold:
            count_compression += 1
        else:
            cleaned_sublist.append(sublist[i - 1])

    # Compression algorithm
    for i in range(len(cleaned_sublist)):
        if i%n==0 and i+n<=len(cleaned_sublist):
            petite_liste=cleaned_sublist[i:i+n]
            count_compression, plot_compression_liste = calcul_general(petite_liste,count_compression,plot_compression_liste)
        elif i+n>len(cleaned_sublist):
            count_compression += len(cleaned_sublist)-i
            break

    compression_list.append(count_compression)
    len_of_all_plot_compression_list_percentage.append((compression_list[-1]*100)/120)

print(compression_list)
print(len_of_all_plot_compression_list_percentage)
print(isSick)

## Affichage

# Créer une figure
fig = go.Figure()

# Extraire les coordonnées x, y et z de plot_compression_list
x_red = [point[0] for point in plot_compression_liste]
z_red = [point[1] for point in plot_compression_liste]
y_red = [point[2] for point in plot_compression_liste]


tmp_list = []
colors = ['blue', 'green', 'red', 'purple', 'orange', 'yellow']

for i in range(len(position_data)):
    if i % 120 == 0:
        tmp_list.append(position_data[i])

x_green = [point[0] for point in tmp_list]
z_green = [point[1] for point in tmp_list]
y_green = [point[2] for point in tmp_list]



#Parcourir chaque sous-liste dans position_data_list
for sublist in position_data_list:
    # Extraire les coordonnées x, y et z de la sous-liste
    x = [point[0] for point in sublist]
    z = [point[1] for point in sublist]
    y = [point[2] for point in sublist]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(color='blue')))

fig.add_trace(go.Scatter3d(x=x_red, y=y_red, z=z_red, mode='markers', marker=dict(color='red')))
fig.add_trace(go.Scatter3d(x=x_green, y=y_green, z=z_green, mode='markers', marker=dict(color='green')))

fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))

# Afficher le graphique
fig.show()

# Créer un DataFrame à partir des données
df = pd.DataFrame({'compression': len_of_all_plot_compression_list_percentage, 'isSick': isSick})

# Extraire le nom du fichier d'entrée
filename = os.path.splitext(os.path.basename(csv_file))[0]

# Définir le nom du fichier de sortie
output_filename = f"{filename}_conversion.xlsx"

# Chemin du dossier de sortie
output_folder = "./data/conversion"

# Assurez-vous que le dossier de sortie existe, sinon le créez
os.makedirs(output_folder, exist_ok=True)

# Chemin complet du fichier de sortie
output_path = os.path.join(output_folder, output_filename)

# Exporter le DataFrame vers un fichier Excel
df.to_excel(output_path, index=False)

print(f"Le fichier Excel '{output_filename}' a été créé avec succès dans le dossier '{output_folder}'.")