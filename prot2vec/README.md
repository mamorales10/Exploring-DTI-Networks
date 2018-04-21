# Prot2vec

Contains a trained model, `protVec_100d_3grams.csv`, based on word2vec, which featurizes protein sequences by embedding into a 100 dimensional vector space.
The model was trained using 324,018 protein sequences from Swiss-Prot.

`prot2vec.py` was used to convert the receptor sequences into vectors.
The other csv files contain the generated vector embeddings.

**Reference:**

*Continuous Distributed Representation of Biological Sequences for Deep Genomics and Deep Proteomics* [[paper](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0141287)]
