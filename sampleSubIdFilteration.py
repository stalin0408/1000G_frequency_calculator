file_path = "/home/stalin/integrated_call_male_samples_v3.20130502.ALL.panel"

# Set to store distinct values in 'pop' column
unique_populations = set()

# Read the file and extract distinct values from the 'pop' column
with open(file_path, "r") as file:
    for line in file:
        columns = line.strip().split("\t")
        sample, pop, super_pop, gender = columns  # Unpack columns
        unique_populations.add(pop)  # Add 'pop' column to the set

# Convert the set to a list if needed
unique_populations_list = list(unique_populations)

print(unique_populations_list)

