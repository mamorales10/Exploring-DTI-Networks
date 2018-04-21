import pandas as pd
from multiprocessing import Pool
from tqdm import tqdm
from chembl_webresource_client.new_client import new_client


def fetch_ligs(gene):
    res = target.filter(target_synonym__icontains=gene)
    # Initialize empty data frame
    compounds = pd.DataFrame(columns=columns)
    try:
        t = res[0]['target_chembl_id']
        assays = activity.filter(target_chembl_id=t)
        # Store all activity assays in data frame
        compounds = pd.DataFrame(list(assays))
        compounds = compounds[columns]
        compounds.pchembl_value = compounds.pchembl_value.apply(
                pd.to_numeric, errors='coerce')
        # Remove duplicates and filter out missing values
        compounds = compounds.drop_duplicates(['molecule_chembl_id'])
        compounds = compounds.dropna()
    except:
        compounds = pd.DataFrame(columns=columns)
    # Read data frame with compounds from CHEMBL
    pharos_df = pd.read_csv(receptor_type + "/" + gene + "_ligands.csv")
    pharos_ligs = pharos_df.name
    # Remove duplicates from the compounds data frame
    compounds = compounds.loc[~compounds.molecule_chembl_id.isin(pharos_ligs)]
    # Remove unnecessary columns
    del(pharos_df["id"])
    del(pharos_df["assay_type"])
    # Reorder and rename columns
    cols = pharos_df.columns.tolist()
    cols = cols[1:2] + cols[0:1] + cols[2:]
    pharos_df = pharos_df[cols]
    pharos_df.columns = columns
    # Combine data frames
    pharos_df = pharos_df.append(compounds)
    # Save to csv
    pharos_df.to_csv(gene + "_ligands.csv")


if __name__ == "__main__":
    receptor_type = "GPCRs"
    gene_names = pd.read_csv("receptor_ids/" + receptor_type +
                             ".csv").iloc[:, 1]
    target = new_client.target
    activity = new_client.activity
    columns = ['molecule_chembl_id', 'canonical_smiles', 'pchembl_value']
    # Fetch compounds
    pool = Pool(processes=256)
    num_jobs = len(gene_names)
    with tqdm(total=num_jobs) as pbar:
        for i, _ in tqdm(enumerate(
                         pool.imap_unordered(fetch_ligs, gene_names))):
            pbar.update()
