import math

import csv
import pandas as pd
import plotly.graph_objects as go
import os


def distance(point_a, point_b):
    """
    Calculate the Euclidean distance between two points.

    :param point_a: The first point in format [x, y, z].
    :param point_b: The second point in format [x, y, z].
    :return: The Euclidean distance between the two points.
    """
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2 + (point_a[2] - point_b[2]) ** 2)


def define_cylinder(a, b, c, points_list, k, p, rad):
    """
    Create a cylinder passing through two points.

    :param a: The x-component of the vector between the starting and ending points.
    :param b: The y-component of the vector between the starting and ending points.
    :param c: The z-component of the vector between the starting and ending points.
    :param points_list: A list of points in space.
    :param k: The index of the starting point.
    :param p: The index of the ending point.
    :param rad: The radius of the cylinder.
    :return: True if cylinder contains point p, False otherwise.
    """
    eq_cylinder = ((
            ((points_list[p][1] - points_list[k][1]) * c - (points_list[p][2] - points_list[k][2]) * b) ** 2 +
            ((points_list[p][2] - points_list[k][2]) * a - (points_list[p][0] - points_list[k][0]) * c) ** 2 +
            ((points_list[p][0] - points_list[k][0]) * b - (points_list[p][1] - points_list[k][1]) * a) ** 2)) \
                  / (a ** 2 + b ** 2 + c ** 2)

    if eq_cylinder < (rad ** 2):
        return True

    else:
        return False


def calculate_vector_dir(points_list, j, k):
    """
    Calculate the directional vector between two points.

    :param points_list: A list of points in format [[x1, y1, z1], [x2, y2, z2], ...].
    :param j: The index of the first point.
    :param k: The index of the second point.
    :return: The directional vector from point j to point k.
    """
    vector = (points_list[k][0] - points_list[j][0],
              points_list[k][1] - points_list[j][1],
              points_list[k][2] - points_list[j][2])

    return vector


def check_points_in_cylinder(sublist_piece, compression_counter, preserved_points_list):
    """
    Check if points between the first and last points of the sublist_piece are inside the cylinder.

    :param sublist_piece: A portion of lists with a length of 120.
    :param compression_counter: An integer counting the number of times a point is removed because it is inside the cylinder.
    :param preserved_points_list: The list of points that are kept to obtain the final list of all points.
    :return: A tuple containing the updated compression_counter and the list of preserved points.
    """
    # Append the first point of the sublist_piece to preserved_points_list
    preserved_points_list.append(sublist_piece[0])

    # Calculate the directional vector between the first and last points of the sublist
    a, b, c = calculate_vector_dir(sublist_piece, 0, -1)  # VEC DIR

    # Check if each point between the first and last of the sublist is inside the cylinder
    # If inside, increment compression_counter, else add the point to the list of preserved points
    for p in range(1, len(sublist_piece)):
        if define_cylinder(a, b, c, sublist_piece, 0, p, radius):
            compression_counter += 1
        else:
            preserved_points_list.append(sublist_piece[p])

    # Return the compression count and the list of preserved points
    return compression_counter, preserved_points_list


# Data file - Time, X, Y, Z, Rotation, isSick
csv_file = "./cyril.csv"  # Test file
# csv_file = "../data_collected/labyrinth/participant_1.csv"

position_data = []  # X, Y, Z
isSick_data = []  # isSick

# Extract data [X, Y, Z] and [isSick] from the file
with open(csv_file, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    next(csv_reader)  # Ignore titles
    for line in csv_reader:
        x = float(line[1])
        y = float(line[2])
        z = float(line[3])
        is_sick = int(line[5])
        position_data.append([x, y, z])  # Put [x, y = 0, z] for the Labyrinth, Unity measurement not always as 0
        isSick_data.append(is_sick)

# Cut list in sublist of 120 elements, 120 is the number of movements collected for 1 answer of sickness
sublist_length = 120  # We keep it as a variable in case we need to change it

position_data_list = []
isSick_data_list = []

# Divide position data_collected into 120 elements
for i in range(0, len(position_data), sublist_length):
    sublist = position_data[i:i + sublist_length]  # 0:119 - 120:239 - 240:359...
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

# Clean point too close of x distance
distance_threshold = 0.00000000001

# Radius of the cylinder between two points
radius = 1.5

# n < 120, n is the number of points between two samples
# Increasing too much n loses precision (too global), decreasing it too much is too local
# Also for n, you will for sure keep at least one point every n points, try to change it and watch on plots
n = 10

# Compression percentage list, one compression value for each sublist of 120 elements
compression_percentage = []

# Keep in track the number of points removed for each sublist of 120 element
# Also used to calculate compression_percentage
compression_list = []
stored_points = []  # Total of points we keep

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
        if i % n == 0 and i + n <= len(cleaned_sublist):
            sublist_fragment = cleaned_sublist[i:i + n]
            count_compression, stored_points = check_points_in_cylinder(sublist_fragment, count_compression, stored_points)
        elif i + n > len(cleaned_sublist):
            count_compression += len(cleaned_sublist) - i
            break

    compression_list.append(count_compression)
    compression_percentage.append((compression_list[-1] * 100) / 120)

print(compression_list)
print(compression_percentage)
print(isSick)

# Create a figure
fig = go.Figure()

# Extract x, y, and z coordinates from plot_compression_list
x_red = [point[0] for point in stored_points]
z_red = [point[1] for point in stored_points]
y_red = [point[2] for point in stored_points]

# Selects only frontier points between sublists of 120 elements by applying modulo 120 to the index
points_modulo_120 = []
colors = ['blue', 'green', 'red', 'purple', 'orange', 'yellow']

for i in range(len(position_data)):
    if i % 120 == 0:
        points_modulo_120.append(position_data[i])

x_green = [point[0] for point in points_modulo_120]
z_green = [point[1] for point in points_modulo_120]
y_green = [point[2] for point in points_modulo_120]

# Iterate over each sublist in position_data_list
for sublist in position_data_list:
    # Extract x, y, and z coordinates from the sublist
    x = [point[0] for point in sublist]
    z = [point[1] for point in sublist]
    y = [point[2] for point in sublist]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(color='blue')))

fig.add_trace(go.Scatter3d(x=x_red, y=y_red, z=z_red, mode='markers', marker=dict(color='red')))
fig.add_trace(go.Scatter3d(x=x_green, y=y_green, z=z_green, mode='markers', marker=dict(color='green')))

fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))

# Display the graph
fig.show()

# Create a DataFrame from the data
df = pd.DataFrame({'compression': compression_percentage, 'isSick': isSick})

# Extract the input file name
filename = os.path.splitext(os.path.basename(csv_file))[0]

# Define the output file name
output_filename = f"{filename}_conversion.xlsx"

# Output folder path
output_folder = "./data/conversion"

# Ensure that the output folder exists, otherwise create it
os.makedirs(output_folder, exist_ok=True)

# Full path of the output file
output_path = os.path.join(output_folder, output_filename)

# Export the DataFrame to an Excel file
df.to_excel(output_path, index=False)

print(f"The Excel file '{output_filename}' has been successfully created in the folder '{output_folder}'.")
