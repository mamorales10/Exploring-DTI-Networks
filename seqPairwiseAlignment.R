#import Biostrings and seqinr libraries
library(Biostrings)
library (seqinr)
library(tools)

# reading in seq files into a seq vector
f <- length(list.files(pattern = "*.txt"))
seqs = c()

for (i in list.files(pattern = "*.txt")){
  s <-read.fasta(file=i, seqtype="AA", as.string = TRUE, seqonly = TRUE)
  seqs <- c(seqs, s)
}

# parsing proteins IDs to name rows and cols of a matrix
IDs = c()
for (i in list.files(pattern = "*.txt")){
  n <-file_path_sans_ext(i)
  IDs <- c(IDs, n)
}



score.psa = c()
for (j in 1:length(seqs)){
  psa <- pairwiseAlignment(seqs[[1]], seqs[[j]], type = "local", substitutionMatrix = BLOSUM62, gapOpening = 10, gapExtension = 0.5, scoreOnly = TRUE)
  score.psa <- c(score.psa, psa)
}

targetPairSeqAlign <- matrix(score.psa, nrow = 1, ncol = f)

for (i in 2:length(seqs)) {
  score.psa = c()
  for (j in 1:length(seqs)){
    psa <- pairwiseAlignment(seqs[[i]], seqs[[j]], type = "local", substitutionMatrix = BLOSUM62, gapOpening = 10, gapExtension = 0.5, scoreOnly = TRUE)
    score.psa <- c(score.psa, psa)
  }
  targetPairSeqAlign <- rbind(targetPairSeqAlign, score.psa)
 
}

# Name columns and rows of the matrix
colnames(targetPairSeqAlign) <- IDs
rownames(targetPairSeqAlign) <- IDs

write.csv(targetPairSeqAlign, file = "targetPairwiseAlign.csv")





