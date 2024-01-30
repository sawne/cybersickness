import csv

# Create a diagonal cylinder
def cylinder_define(px, py, pz):
    eq_cylinder = (px ** 2 + py ** 2 + pz ** 2) - \
               ((
                        vector[0] * (px - arriving_point[0])
                        + vector[1] * (py - arriving_point[1])
                        + vector[2] * (pz - arriving_point[2])) ** 2
                / (vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2))

    return eq_cylinder

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

print(position_data_sublist)
print(isSick_data_sublist)

compressed_list = []

# Pour chaque liste de "sublist_length" éléments on compresse selon les déplacements du joueur
for sublist in position_data_sublist:
    i = 0
    compressed_sublist = []
    compression_finished = False

    # Point de départ et d'arrivée du cylindre, point de départ étant fixé au dernier point position du joueur
    starting_point = sublist[0][-1]
    arriving_point = sublist[0][i]
    vector = arriving_point - starting_point

    #
    while not compression_finished:
        check_point = sublist[0][i + 1]
        result = cylinder_define(check_point)

        if result = :
            continue
        else:
            i += 1
            arriving_point = sublist[0][i]

    # On ajoute le dernier point manuellement
    compressed_sublist.append(sublist[0][-1])
    compressed_list.append(compressed_sublist)



