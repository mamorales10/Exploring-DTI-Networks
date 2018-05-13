library(geigen)
library(RANN)
library(matrixcalc)

#set into more reasonable values
lamda1=0.1
lamda2=0.1
d=50 # dimension of entities after being mapped

#read adjacent matrix, Aij=1 if ui and vj are connected, u is ligands
A=read.table("44x100_nr_lig_interactions.csv")
A[A>0]=1
#transpose A if necessary to make sure rows are ligands
A=as.matrix(t(A))

######################

#define degree matrices, diagonal elements=number of interactions 
D1=apply(A, 1, sum) #diagonals
D2=apply(A, 2, sum)
Du=diag(D1)
Dv=diag(D2)

#kernel matrices
Ku=read.table("100x100_ligands_cosine_similarity.csv")
Ku=as.matrix(Ku)
#Kv=read.table("44x44_nr_cosine_similarity.csv")
Kv=read.table("nuclear_disease_tanimoto1.csv", sep=",")
Kv=as.matrix(Kv)


left=rbind(cbind(Ku%*%Du%*%Ku+lamda1*Ku, -Ku%*%A%*%Kv), 
      cbind(-Kv%*%t(A)%*%Ku,Kv%*%Dv%*%Kv+lamda2*Kv))


right=rbind(cbind(Ku%*%Ku, matrix(0, dim(Ku)[1],dim(Kv)[2])), 
           cbind(matrix(0, dim(Kv)[1],dim(Ku)[2]),Kv%*%Kv))


#symmetric true or false?
obj=geigen(left, right, only.values=FALSE)

#eigenvalues in decreasing order
eigenvalues=obj$values

#eigen vectors are stored in column vectors
eigenvectors=obj$vectors
eigenvectors=eigenvectors[,eigenvalues>0]

#get eigenvectors corresponding to d smallest eigenvalues
subeigenvectors=eigenvectors[, (dim(eigenvectors)[2]-d+1):dim(eigenvectors)[2]]

#get alphas and betas
alphas=subeigenvectors[1:dim(Ku)[1],]
betas=subeigenvectors[(dim(Ku)[1]+1):dim(subeigenvectors)[1],]

#################################################################################

#construct entities for old drugs, rows are points
ff=t(alphas)%*%Ku
ff=t(ff)
#construct entities for old proteins
gg=t(betas)%*%Kv
gg=t(gg)

#construct edge matrix
Edge=A

#prediction
Kunew=read.table("200x200_ligands_cosine_similarity.csv")
Kunew=as.matrix(Kunew)
Kunew=Kunew[1:100, 101:200]

#mapping new drugs into d-dimension entities network
#entities are stored in rows of ffnew matrix
ffnew=t(alphas)%*%Kunew
ffnew=t(ffnew)

#initialize new interaction matrix Edgenew
#rows denote new drugs, columns denote old proteins
Edgenew=matrix(0, 100,44)
#search protein entities in gg that are close to ffnew


delta= 0.4#set into a reasonalble value
result=nn2(gg, ffnew, k=1, searchtype = "radius",  radius = delta)
result$nn.idx
#correct rate
length(which(result$nn.idx==benchmark))/length(benchmark)

data.frame(result$nn.idx,benchmark)
###################################################################
Anew=read.table("44x200_nr_lig_interactions_full.csv")
Anew=t(as.matrix(Anew))
Anew=Anew[101:200,]
Anew[Anew>0]=1

benchmark=vector(length = 0)

for (i in 1:dim(A)[1]) {
  benchmark=c(benchmark,which(A[i,]!=0,arr.ind = TRUE))
}

