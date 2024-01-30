import csv

# Chemin vers le fichier CSV
csv_file = '/home/cyril/Downloads/PlayerData_20240129102610.csv'

# Listes pour stocker les données
position_data = []
isSick_data = []

# Lecture du fichier CSV et extraction des données
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

# Nombre d'éléments par sous-liste
sublist_length = 120

# Liste pour stocker les sous-listes de XYZ et isSick
position_data_sublist = []
isSick_data_sublist = []

# Diviser les données XYZ en sous-listes
for i in range(0, len(position_data), sublist_length):
    sublist = position_data[i:i + sublist_length]
    if len(sublist) == sublist_length:
        position_data_sublist.append(sublist)

# Diviser les données isSick en sous-listes
for i in range(0, len(isSick_data), sublist_length):
    sublist = isSick_data[i:i + sublist_length]
    if len(sublist) == sublist_length:
        isSick_data_sublist.append(sublist)

compression_finished = False

for sublist in position_data_sublist:
    starting_point = sublist[0][-1]
    arriving_point = sublist[0][0]

    while not compression_finished:
        compression_finished = True


