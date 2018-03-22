for (i in 1:nrow(GPCRs[,2])){
  download.file(paste("http://www.uniprot.org/uniprot/", 
                      GPCRs[i,2],".fasta",sep=""),
                paste(GPCRs[i,2],".txt",sep=""))
  
}

for (i in 1:nrow(ion_channels[,2])){
  download.file(paste("http://www.uniprot.org/uniprot/", 
                      ion_channels[i,2],".fasta",sep=""),
                paste(ion_channels[i,2],".txt",sep=""))
  
}

for (i in 1:nrow(kinases[,2])){
  download.file(paste("http://www.uniprot.org/uniprot/", 
                      kinases[i,2],".fasta",sep=""),
                paste(kinases[i,2],".txt",sep=""))
  
}

for (i in 1:nrow(nuclear_hormone_receptors[,2])){
  download.file(paste("http://www.uniprot.org/uniprot/", 
                      nuclear_hormone_receptors[i,2],".fasta",sep=""),
                paste(nuclear_hormone_receptors[i,2],".txt",sep=""))
  
}
