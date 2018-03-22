import csv
import json
from tqdm import tqdm
from urllib.request import urlopen

# A simple script to retrieve ligand structures (as SMILES format) for
# a given target.
#   Usage: python fetch_ligand.py TARGET
# where TARGET can be gene (e.g., abl1), UniProt accession (e.g., P00519),
# ENSEMBL (e.g., ENSP00000361423), etc

pharos = "https://pharos.nih.gov/idg/api/v1/targets/"


def fetch_ligand(target):
    # List for storing ligand data with header for csv file
    lig_data = [("id", "smiles", "name", "assay_type", "activity_value")]
    # Fetch target
    req = urlopen(pharos + target)
    target_dict = json.loads(req.read())
    # Retrieve ligand links for this target
    print("Fetching ligands for target: ", target)
    req = urlopen(pharos + '{0}'.format(target_dict['id']) +
                  "/links(kind=ix.idg.models.Ligand)")
    link = json.loads(req.read())
    for l in tqdm(link):
        name = ""
        # Extract ligand name
        for p in l['properties']:
            if p['label'] == "IDG Ligand" or p['label'] == "IDG Drug":
                name = p['term']
                break
        # Extract ligand activity
        for p in l['properties']:
            if p['label'] in {"Ki", "Kd", "IC50", "EC50", "AC50", "Potency"}:
                assay = p['label']
                value = p['numval']
                break
        # Extract SMILES string
        req = urlopen(l['href'] + "/properties(label=CHEMBL Canonical SMILES)")
        ligand = json.loads(req.read())
        # Add information to list
        lig_data.append((ligand['id'], ligand['text'], name, assay, value))
    # Save all data to a CSV file
    with open(target + "_ligands.csv", 'w') as out_file:
        writer = csv.writer(out_file, delimiter=',')
        writer.writerows(lig_data)


if __name__ == "__main__":
    import sys
    fetch_ligand(sys.argv[1])
