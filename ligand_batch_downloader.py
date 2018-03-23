# A script for reading a column of receptor IDs from a csv file,
# and batch downloading the list of ligands associated with them.
# Uses fetch_ligands.py

from fetch_ligands import fetch_ligand
import pandas as pd
import os

""" Location of csv files. Modify this part if necessary. """
root = "data/receptor_ids/"
csv_files = ["GPCRs.csv", "kinases.csv", "ion-channels.csv",
             "nuclear-hormone-receptors.csv"]

for csv in csv_files:
    # Read csv file into data frame.
    df = pd.read_csv(root + csv)
    # Extract Uniprot IDs
    uniprot_ids = df['Uniprot ID']
    # Fetch ligands
    output_dir = "ligand_ids/" + csv.split(".")[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for ID in uniprot_ids:
        fetch_ligand(ID, output_dir)
