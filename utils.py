import csv
import math
import pandas as pd

import openpyxl
from openpyxl.utils import get_column_letter
from datetime import datetime
import os


# Return distance between two points in format [x,y,z]
def distance(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2 + (point_a[2] - point_b[2]) ** 2)


# Create a cylinder between two points
# j = k (start point) and l = i (end point)
def define_cylinder(pa, pb, pc, points_list, j, o):
    eq_cylinder = (points_list[o][0] ** 2 + points_list[o][1] ** 2 + points_list[o][2] ** 2) - \
                  ((
                           pa * (points_list[o][0] - points_list[j][0])
                           + pb * (points_list[o][1] - points_list[j][1])
                           + pc * (points_list[o][2] - points_list[j][2])) ** 2
                   / ((pa ** 2) + (pb ** 2) + (pc ** 2)))

    return eq_cylinder


# Calculate the vector director between two points
def calculate_vector_dir(points_list, m):
    vector = (points_list[m + 1][0] - points_list[m][0],
              points_list[m + 1][1] - points_list[m][1],
              points_list[m + 1][2] - points_list[m][2])

    return vector


# csv_file = './PlayerData_20240129102610.csv'
csv_file = './Fleur2.csv'

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
errors = [1000, 2000, 3000, 5000]
count_compression_compilation = []

for error in errors:
    count_compression = 0
    count_compression_list = []
    # For each sublist we compress movement player list and calculate the compression ratio
    for sublist in position_data_list:
        cleaned_sublist = []  # Sublist without points too close together
        count_compression = 1  # First point

        # Clean points too close together
        for i in range(1, 120):
            if distance(sublist[i], sublist[i - 1]) < distance_threshold:
                count_compression += 1
            else:
                cleaned_sublist.append(sublist[i])

        # Compression algorithm
        k, i = (0, 2)
        size = len(cleaned_sublist)
        while k < size:
            if k == size - 1:
                count_compression += 1
                k = size

            if k == size - 2:
                count_compression += 2
                k = size

            else:
                a, b, c = calculate_vector_dir(cleaned_sublist, k)  # VEC DIR: sublist[k] / sublist[i]
                # Check if clean_sublist[i - 1] is inside the cylinder
                # print(define_cylinder(a, b, c, cleaned_sublist, k, i))
                if define_cylinder(a, b, c, cleaned_sublist, k, i) < error:     # À update // Point [i -1] inside cylinder?
                    count_compression += 1
                    if i < (size - 1):
                        i += 1
                    else:
                        k = size

                else:
                    k = i - 1
                    i = k + 2

        count_compression_list.append(count_compression)

    count_compression_compilation.append(count_compression_list)

# Get each compression counter in %
for sublist in count_compression_compilation:
    # Be careful to give an int in input
    for i in range(len(sublist)):
        sublist[i] = (sublist[i] * 100) / 120

print(isSick)
print(count_compression_compilation)

# Créer un dictionnaire pour stocker les données
data = {'isSick': isSick}

# Ajouter les colonnes pour chaque valeur dans errors
for i, error in enumerate(errors):
    print(f'error_{error} : {count_compression_compilation[i]}\n')



# # Créer un DataFrame à partir du dictionnaire de données
# df = pd.DataFrame(data)
#
# # Exporter le DataFrame vers un fichier Excel
# df.to_excel('donnees_traitees.xlsx', index=False)