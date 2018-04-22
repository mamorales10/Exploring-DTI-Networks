import glob
import pandas as pd


def get_ligands(folder):
    data = glob.glob(folder + "/*.csv")
    ligs = pd.DataFrame()
    for receptor in data:
        temp_df = pd.read_csv(receptor).iloc[:, 1:3]
        ligs = pd.concat([ligs, temp_df], axis=0)
    ligs = ligs.drop_duplicates(['molecule_chembl_id'])
    return ligs


types = ["GPCRs", "kinases", "ion-channels", "nuclear-hormone-receptors"]
all_ligs = pd.DataFrame()
for item in types:
    print("Joining ligands for", item)
    results = get_ligands(item)
    all_ligs = pd.concat([all_ligs, results], axis=0)
    all_ligs = all_ligs.drop_duplicates(['molecule_chembl_id'])
    print("Number of unique ligands:", len(all_ligs))

print("Done. Saving data to csv.")
all_ligs.to_csv("all_unique_ligands.csv", index=False)
