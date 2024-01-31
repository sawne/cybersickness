import csv


# Créer un cylindre oblique
# Variable coordinates du point
# Variable ce qui va calculer le cylindre
# j = k et l = i
def define_cylinder(pa, pb, pc, points_list, j, o):
    eq_cylinder = (points_list[o][0] ** 2 + points_list[o][1] ** 2 + points_list[o][2] ** 2) - \
                  ((
                           pa * (points_list[o][0] - points_list[j + 1][0])
                           + pb * (points_list[o][1] - points_list[j + 1][0])
                           + pc * (points_list[o][2] - points_list[j + 1][0])) ** 2
                   / ((pa ** 2) + (pb ** 2) + (pc ** 2)))

    return eq_cylinder


def calculate_vector_dir(points_list, m):
    # Définir le vecteur entre nos deux points
    vector = (points_list[m + 1][0] - points_list[m][0],
              points_list[m + 1][1] - points_list[m][1],
              points_list[m + 1][2] - points_list[m][2])

    return vector


# Chemin vers le fichier CSV
csv_file = '../PlayerData_20240129102610.csv'

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
position_data_list = []
isSick_data_list = []

# Diviser les données XYZ en sous-listes
for i in range(0, len(position_data), sublist_length):
    sublist = position_data[i:i + sublist_length]
    if len(sublist) == sublist_length:
        position_data_list.append(sublist)

# Diviser les données isSick en sous-listes
for i in range(0, len(isSick_data), sublist_length):
    sublist = isSick_data[i:i + sublist_length]
    if len(sublist) == sublist_length:
        isSick_data_list.append(sublist)

print(position_data_list)
print(isSick_data_list)

compressed_list = []

# Pour chaque liste de "sublist_length" éléments on compresse selon les déplacements du joueur
for sublist in position_data_list:
    error = 1000

    compressed_sublist = 1

    k, i = (0, 0)
    len_sublist = len(sublist)
    while k < len_sublist:
        if k == len_sublist - 2:
            compressed_sublist += 2

        elif k == len_sublist - 1:
            compressed_sublist += 1

        else:
            a, b, c = calculate_vector_dir(sublist, k)
            while define_cylinder(a, b, c, sublist, k, i) <= error:
                i += 1

            k = i - 1
            i = k

            compressed_sublist += 1

print(compressed_list)
