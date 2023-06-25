import requests
import csv
import json
import pandas as pd
import re

def diseaseTrait_Ancestry(snp_id):

    url = f'https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{snp_id}/studies'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        for study in data['_embedded']['studies']:
            output = {
                'Disease Trait': study['diseaseTrait'],
                'Ancestry': study['ancestries']
            }
            print(json.dumps(output, indent=4))
    else:
        print(f'Request failed with status code {response.status_code}')

def creatediseaseTrait_Neuro_Brain_Behavior():
    # Open the text file for reading
    file_path = input("Go to https://github.com/cr27 and download my 23&Me .txt file."
                      "\nEnter filepath to your downloaded 23&Me .txt file")
    with open(file_path, 'r') as infile:

        with open('23ME.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile)

            # Loop over each line in the text file and write it to the CSV file
            for line in infile:
                writer.writerow([line.strip()])

    # Load the CSV file into a pandas DataFrame
    genome_data_test = pd.read_csv('23ME.csv', sep='|', skiprows=19)
    print(genome_data_test.columns)

    data = []
    for index, row in genome_data_test.iterrows():
        items = row[0].split("\t")
        data.append(items)

    columns = "rsid|chromosome|position|genotype".split("|")
    df = pd.DataFrame(data=data, columns=columns)
    print(df.head())
    df.to_csv("reformatted_23ME.csv")


    print("Download gwas_Catalog from this url:" + "https://www.ebi.ac.uk/gwas/api/search/downloads/alternative")
    print("Make Sure you have the file path and it is correct");
    gwas_data = pd.read_csv(r#insert GWAS .tsv file path here, sep='\t')
    gwas_data = gwas_data.rename(columns={'SNPS': 'rsid'})

    # Load 23andMe data
    print("Make Sure you have the file path and it is correct");
    me_data = pd.read_csv(#insert reformatted 23andMe csv path here)

    # Merge the two datasets on the rsid column
    merged_data = pd.merge(me_data, gwas_data, on="rsid", how="inner")

    # Filter rows with "brain", "behavior", or "neuro" in the disease_trait column
    merged_data = merged_data[merged_data["DISEASE/TRAIT"].str.lower().str.contains("brain|behavior|neuro", regex=True)]

    # Save the filtered data to a new CSV file
    merged_data.to_csv("GWASplus23&ME.csv", index=False)
    print(merged_data["DISEASE/TRAIT"])
if __name__ == '__main__':
    creatediseaseTrait_Neuro_Brain_Behavior()
    #rsid is your SNP ID, uncomment the code below to look up ancestry and disease trait associated with rsid
    snp_id = input('Enter your SNP ID: ')  # replace with your SNP ID
    diseaseTrait_Ancestry(snp_id)
