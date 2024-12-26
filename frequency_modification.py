import os
import pandas as pd
import glob

# Define a function to process a single frequency file
def process_frequency_file(file_path, population):

    valid_lines = []
    # Open the frequency file and read line by line
    with open(file_path, 'r') as file:
        for line in file.readlines():
            # Split the line by tab (\t) delimiter
            fields = line.strip().split('\t')
            # Check if the line has the expected number of fields
            if len(fields) == 6:  # Assuming 6 columns
                allele_freq_parts_1 = fields[-1].split(':')  # Splitting the last column
                allele_freq_parts_2 = fields[-2].split(':')  # Splitting the second-last column

                extended_parts = allele_freq_parts_1 + allele_freq_parts_2  # Concatenate the lists
                fields += extended_parts  # Extend the fields with additional parts
                valid_lines.append(fields)

    valid_lines_filtered = [line for line in valid_lines if len(line) == 10]

    # Initialize the dictionary
    Dict = {'CHROM': [], 'POS': [], 'ALT_allele': [], 'REF_allele': [], 'REF': []}
    Dict[population] = []
    print(Dict)
    # Iterate over valid lines and populate the dictionary
    for i in range(len(valid_lines_filtered)):
        Dict['CHROM'].append(valid_lines_filtered[i][0])
        Dict['POS'].append(valid_lines_filtered[i][1])
        Dict['ALT_allele'].append(valid_lines_filtered[i][-4])
        #for population in populations:
        #    print(population)
        Dict[population].append(valid_lines_filtered[i][-3])
        Dict['REF_allele'].append(valid_lines_filtered[i][-2])
        Dict['REF'].append(valid_lines_filtered[i][-1])

    print("Processing completed:", population)
    return Dict

# Specify the directory containing frequency files
directory = '/home/stalin/Downloads/chrFileList/chr_15_frq'

# List of populations
populations = ['ACB','ASW','BEB','CDX','CEU','CHB','CHS','CLM','ESN','FIN','GBR','GIH','GWD','IBS','ITU','JPT','KHV','LWK','MSL','MXL','PEL','PJL','PUR','STU','TSI','YRI','AFR','AMR','EAS','EUR','SAS','W']

# Initialize an empty dictionary to store concatenated data
concatenated_dict = {'CHROM': [], 'POS': [], 'ALT_allele': [], 'REF_allele': [], 'REF': []}
for population in populations:
    concatenated_dict[population] = []
frequency_file_list = glob.glob(f'{directory}/*.frq')
chrom_pos_extended = False
# Iterate through the files in the directory
for file_path in frequency_file_list:
    file_name = file_path.split("/")[-1]
    # Flag to check if CHROM and POS keys have been extended
    for population in populations:
        print(population)
        if population in file_name:
            # Process the frequency file for the current population
            print("population:", population)
            if population in file_name:
                population_dict = process_frequency_file(file_path, population)
                # Append the data for the current population to the concatenated dictionary
                if not chrom_pos_extended:  # Check if CHROM and POS keys have been extended
                    concatenated_dict['CHROM'].extend(population_dict['CHROM'])
                    concatenated_dict['POS'].extend(population_dict['POS'])
                    concatenated_dict['ALT_allele'].extend(population_dict['ALT_allele'])
                    concatenated_dict['REF_allele'].extend(population_dict['REF_allele'])
                    concatenated_dict['REF'].extend(population_dict['REF'])
                    chrom_pos_extended = True
                concatenated_dict[population].extend(population_dict[population])

# Now, you can loop through the concatenated_dict.keys() and print the lengths
for key in concatenated_dict.keys():
    print(f"Length of {key}: {len(concatenated_dict[key])}")

# Create a DataFrame from the concatenated dictionary
df = pd.DataFrame(concatenated_dict)

# Specify the output file path for the CSV file
output_csv_file = 'all_columns_chr_15.csv'

# Write data to CSV file
df.to_csv(output_csv_file, index=False)
