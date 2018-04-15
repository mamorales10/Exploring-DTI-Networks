# Data used in this project

## ligand_smiles
Contains the ligand id, SMILES string, and binding affinity for each ligand associated with every protein in the Pharos data set.

## pfam_hits
XML results from running pfam on the protein sequences

## pharos_data
All receptor data downloaded from Pharos. Contains:
 - target ids
 - uniprot keywords
 - publication PubMed IDs
 - pathways
 - Go germs
 - expression
 - diseases

## receptor_ids
Contains Uniprot ids and gene names for receptors from the four major classes of druggable proteins: GPCRs, kinases, ion channels, and nuclear hormone receptors. The data was downloaded from [Pharos](https://pharos.nih.gov), and the receptors were filtered to include only those within the **Tclin** and **Tchem** categories, meaning that they have a sufficient number of known interacting compounds.

## sequences
Contains target sequences, downloaded from [UniProt](http://www.uniprot.org/).
