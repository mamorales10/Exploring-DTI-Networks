#This function will make a interaction matrix based on ligands files in <directory> folder
interactionMatrix=function(directory){
  directoryPath=paste(directory, "/", sep = "")
  Filenames=list.files(path = directoryPath)
  
  #read file names as Protein names
  Alist=vector(length = length(Filenames))
  for (i in 1:length(Filenames)) {
   Alist[i]=strsplit(Filenames[i],split='_', fixed=TRUE)[[1]][1]
  }

  #Read all drug ids
  Blist=c()
  for (j in 1: length(Filenames)){
    Blist=c(Blist,read.csv(file=paste(directoryPath,Filenames[j], sep = ""))[,1])
  }
  Blist=unique(Blist)

  #build an empty interaction matrix
  interaction=data.frame(matrix(ncol = length(Alist), nrow = length(Blist)))
  colnames(interaction)=Alist
  rownames(interaction)=Blist

  #fill activity value in the interaction matrix
  for (j in 1: length(Filenames)){
    temp=read.csv(file=paste(directoryPath,Filenames[j], sep = ""))
    id=temp[,1]
    activity=temp[,5]
    interaction[as.character(id),j]=activity
  }

  write.csv(interaction, file =paste(directory,"Interaction.csv", sep = ""))
}

interactionMatrix("GPCRs")
interactionMatrix("ion-channels")
interactionMatrix("kinases")
interactionMatrix("nuclear-hormone-receptors")
