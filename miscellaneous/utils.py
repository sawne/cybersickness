import csv
import math
import pandas as pd

import openpyxl
from matplotlib import pyplot
from openpyxl.utils import get_column_letter
from datetime import datetime
import os

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Return distance between two points in format [x,y,z]
def distance(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2 + (point_a[2] - point_b[2]) ** 2)


# Create a cylinder between two points
# j = k (start point) and o = i (end point)
def define_cylinder(pa, pb, pc, points_list, j, o, rad, compression):

    eq_cylinder = ((
        ((points_list[o - 1][1] - points_list[j][1]) * c - (points_list[o - 1][2] - points_list[k][2]) * b)**2 +
        ((points_list[o - 1][2] - points_list[k][2]) * a - (points_list[o - 1][0] - points_list[k][0]) * c)**2 +
        ((points_list[o - 1][0] - points_list[k][0]) * b - (points_list[o - 1][1] - points_list[k][1]) * a)**2)) \
                  / (a ** 2 + b ** 2 + c ** 2)

    # if eq_cylinder == 0: print(" k = ", j, "i = ", o)
    # print(eq_cylinder, " < ", (rad ** 2 * (a ** 2 + b ** 2 + c ** 2)))

    if eq_cylinder < (rad ** 2):
        return True

    else:
        return False



# Calculate the vector director between two points
def calculate_vector_dir(points_list, m):
    vector = (points_list[m + 1][0] - points_list[m][0],
              points_list[m + 1][1] - points_list[m][1],
              points_list[m + 1][2] - points_list[m][2])

    return vector


# csv_file = './PlayerData_20240129102610.csv'
csv_file = 'cyril.csv'

position_data = []
isSick_data = []

# Extract data
with open(csv_file, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    next(csv_reader)  # Ignorer l'en-tête
    for line in csv_reader:
        x = float(line[1])
        y = float(line[2])
        z = float(line[3])
        is_sick = int(line[5])
        position_data.append([x, y, z])
        isSick_data.append(is_sick)

# Cut list in sublist of 120 elements, 120 is the number of movements collected for 1 answer of sickness
sublist_length = 120    # We keep it as a variable in case we need to change it

position_data_list = []
isSick_data_list = []

# Divide position data into 120 elements
for i in range(0, len(position_data), sublist_length):
    sublist = position_data[i:i + sublist_length]   # 0:119 - 120:239 - 240:359...
    if len(sublist) == sublist_length:  # if sublist has not 120 elements it's too short to keep it
        position_data_list.append(sublist)

# Divide isSick into 120 elements
for i in range(0, len(isSick_data), sublist_length):
    sublist = isSick_data[i:i + sublist_length]
    if len(sublist) == sublist_length:
        isSick_data_list.append(sublist)

# Keep only 1 example of isSick data
isSick = []
for sublist in isSick_data_list:
    isSick.append(sublist[0])

# print(position_data_list)
# print(isSick)

# Clean point too close of 0.3 distance
distance_threshold = 0.3

# Try different metrics
radius = 1.1

count_compression = 0
compression_list = []

plot_compression_list = []
len_of_all_plot_compression_list_percentage = []
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
    k, i = (0, 2)
    size = len(cleaned_sublist)
    while k < size:
        if k == size - 1:
            count_compression += 1
            break

        if k == size - 2:
            count_compression += 2
            break

        else:
            a, b, c = calculate_vector_dir(cleaned_sublist, k)  # VEC DIR: sublist[k] / sublist[i]
            # Check if clean_sublist[i - 1] is inside the cylinder
            if define_cylinder(a, b, c, cleaned_sublist, k, i, radius, count_compression) is True:
                count_compression += 1
                if i < (size - 1):
                    i += 1
                else:
                    break

            else:
                plot_compression_list.append(sublist[i - 1])
                k = i - 1
                i = k + 2

    compression_list.append(count_compression)
    print(len(plot_compression_list))
    len_of_all_plot_compression_list_percentage.append(((120 - len(plot_compression_list)) / 120) * 100)



# print(len(plot_compression_list))

# Créer une figure
fig = plt.figure()

# Créer un nouveau graphique 3D
ax = fig.add_subplot(111, projection='3d')

# Extraire les coordonnées x, y et z de plot_compression_list
x_red = [point[0] for point in plot_compression_list]
z_red = [point[1] for point in plot_compression_list]
y_red = [point[2] for point in plot_compression_list]

tmp_list = []
colors = ['blue', 'green', 'red', 'purple', 'orange', 'yellow']

for i in range(len(position_data)):
    if i % 120 == 0:
        tmp_list.append(position_data[i])

x_green = [point[0] for point in tmp_list]
z_green = [point[1] for point in tmp_list]
y_green = [point[2] for point in tmp_list]

# Ajouter les points rouges au graphique
ax.scatter(x_red, y_red, z_red, c='red')
ax.scatter(x_green, y_green, z_green, c='green')


# # Parcourir chaque sous-liste dans position_data_list
# for sublist in position_data_list:
#     # Extraire les coordonnées x, y et z de la sous-liste
#     x = [point[0] for point in sublist]
#     z = [point[1] for point in sublist]
#     y = [point[2] for point in sublist]
#
#     # Ajouter les points bleus au graphique
#     ax.scatter(x, y, z, c='blue')

# Définir les labels des axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Afficher le graphique
plt.show()



print(len_of_all_plot_compression_list_percentage)


# Get each compression counter in %
compression_list_percentage = []

for i in compression_list:
    compression_list_percentage.append((i * 100) / 120)

# print(compression_list_percentage)
# print(isSick)








# # Créer un DataFrame à partir du dictionnaire de données
# df = pd.DataFrame(data)
#
# # Exporter le DataFrame vers un fichier Excel
# df.to_excel('donnees_traitees.xlsx', index=False)