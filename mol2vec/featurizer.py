import numpy as np
import pandas as pd
import pickle
from rdkit import Chem
from mol2vec.features import mol2alt_sentence
from gensim.models import word2vec
from tqdm import tqdm


# Read data
data = pd.read_csv("all_unique_ligands.csv")
ligands = (Chem.MolFromSmiles(x) for x in data['canonical_smiles'])
# Create new column to store fingerprints
data['words'] = np.zeros(len(data), dtype='object')

print("Generating molecular fingerprints")
i = 0
with tqdm(total=len(data)) as pbar:
    for l in ligands:
        fingerprint = mol2alt_sentence(l, 1)
        data['words'][i] = list(fingerprint)
        i += 1
        pbar.update()
pickle.dump(data, open("fingerprints.pkl", 'wb'))

# Find all unique words
print("Finding unique fingerprints")
all_words = np.array([word for sentence in data['words'] for word in sentence])
unique_words = np.unique(all_words)

# Create a data frame of embeddings
print("Storing embeddings")
model = word2vec.Word2Vec.load('model_300dim.pkl')
embeddings = {}
for word in unique_words:
    try:
        embeddings[word] = model.wv.word_vec(word)
    except:
        embeddings[word] = np.zeros(300)
embeddings = pd.DataFrame(embeddings)
pickle.dump(embeddings, open("embeddings.pkl", 'wb'))

# Create a data frame to store ligand vectors
vectors = {}
print("Generating vectors")
for mol in tqdm(data['molecule_chembl_id']):
    fingerprint = data.loc[data.molecule_chembl_id == mol]['words']
    for sentence in fingerprint:
        components = embeddings[sentence]
        vec = np.sum(components, axis=1)
    vectors[mol] = vec
vectors = pd.DataFrame(vectors).T

print("Writing csv file")
pickle.dump(vectors, open("vectors.pkl", 'wb'))
vectors.to_csv("ligand_vectors.csv")
