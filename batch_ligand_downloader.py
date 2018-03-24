# A script for reading a column of receptor IDs from a csv file,
# and batch downloading the list of ligands associated with them.
# Uses fetch_ligands.py

# USAGE: python bathc_ligand_downloader.py path_to_csv 

from fetch_ligands import fetch_ligand
import pandas as pd
import os
import sys


csv = sys.argv[1]

# Read csv file into data frame.
df = pd.read_csv(csv)
# Extract Uniprot IDs
uniprot_ids = df['Uniprot ID']
# Fetch ligands
output_dir = "ligand_smiles/" + os.path.split(csv)[1].split(".")[0]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
for ID in uniprot_ids:
    fetch_ligand(ID, output_dir)
