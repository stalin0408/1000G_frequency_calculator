# Define paths to input files
frq_file = "/home/stalin/PycharmProjects/pythonProject1/Fresh/all_columns_chr_16.csv"
vcf_file = "/home/stalin/Downloads/chrFileList/ALL.chr16.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf"

# Define output VCF file
output_file = "/home/stalin/sample_test/SubPopAddedChr16.vcf"

# Read data from the .frq file and store it in respective dictionaries
population_data = {}

with open(frq_file, 'r') as file:
    for line in file:
        if not line.startswith('#'):  # Skip header lines
            fields = line.strip().split(',')
            print(len(fields))
            if len(fields) >= 24:  # Ensure all expected fields are present
                (
                    CHROM, POS, ALT_allele, REF_allele, REF, ASW, LWK, YRI, AFR, CHB, CHS,
                    JPT, EAS, GBR, FIN, CEU, IBS, TSI, EUR, CLM, MXL, PUR, AMR, W_AF

                ) = fields
                population_data[f"{CHROM}:{POS}"] = {
                    'ASW': ASW, 'LWK': LWK, 'YRI': YRI, 'CHB': CHB,
                    'CHS': CHS, 'JPT': JPT, 'GBR': GBR, 'FIN': FIN,
                    'CEU': CEU, 'IBS': IBS, 'TSI': TSI, 'CLM': CLM,
                    'MXL': MXL, 'PUR': PUR, 'W': W_AF
                }
            else:
                print("Incomplete line:", line)
        else:
            print("Incomplete line:", line)

# Update the INFO field of the VCF file based on position
with open(vcf_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        if line.startswith('#'):
            # Write header lines to output file
            outfile.write(line)
        else:
            # Extract chromosome, position, and remaining fields from the VCF line
            CHROM, POS, *rest = line.strip().split('\t')

            # Construct new_info field by iterating over all populations
            new_info = ';'.join([f"{key}={value}" for key, value in
                                 [('ASW', ASW), ('LWK', LWK), ('YRI', YRI), ('CHB', CHB),
                                  ('CHS', CHS), ('JPT', JPT), ('GBR', GBR), ('FIN', FIN),
                                  ('CEU', CEU), ('IBS', IBS), ('TSI', TSI), ('CLM', CLM),
                                  ('MXL', MXL), ('PUR', PUR), ('W', W_AF)]])
            # Extract existing INFO field from rest
            existing_info_field = rest[5]
            print("Existing info", existing_info_field)
            #world = 'W=0.00'
            # Append new frequency data to existing INFO field
            updated_info_field = existing_info_field + ';' + new_info #+ ';' + world
            #updated_info_field_modified = updated_info_field.replace("AF=", "W=")
            print("updated_infofield", updated_info_field)
            #print("rest[:5]:", rest[:5], "\nrest[6]:", rest[6:])
            # Update the line with the updated INFO field
            new_line = '\t'.join([CHROM, POS, *rest[:5], updated_info_field, *rest[6:]])

            # Write the modified line to the output file
            outfile.write(new_line + "\n")

print("Population frequency data has been added to the existing INFO field of the VCF file.")
