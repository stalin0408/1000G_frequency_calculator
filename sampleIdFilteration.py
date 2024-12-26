import os

file_path = "/home/stalin/integrated_call_male_samples_v3.20130502.ALL.panel"
output_directory = "/home/stalin/PycharmProjects/pythonProject/1000G_python/Super_population"  # Directory to save grouped files

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Dictionary to store data grouped by 'pop' column
grouped_data = {}

# Read the file and group data by 'pop'
with open(file_path, "r") as file:
    for line in file:
        columns = line.strip().split("\t")
        sample, pop, super_pop, gender = columns  # Unpack columns

        # Add each line's data to the corresponding 'pop' group
        if pop not in grouped_data:
            grouped_data[pop] = []  # Initialize list for a new 'pop' group
        grouped_data[pop].append(columns)  # Add the full row to the group

# Save each group to a distinct file
for pop, rows in grouped_data.items():
    output_file_path = os.path.join(output_directory, f"{pop}_population.txt")
    with open(output_file_path, "w") as output_file:
        for row in rows:
            output_file.write("\t".join(row) + "\n")  # Write each row as a line in the file

print("Data grouped by 'pop' column and saved to separate files.")
