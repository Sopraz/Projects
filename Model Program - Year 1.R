cell_data <- read.csv('cell_data.csv', stringsAsFactors=TRUE)
cell_data_ad <- read.csv('cell_data_additional.csv', stringsAsFactors=TRUE)
donor_info <- read.csv('donor_info.csv', stringsAsFactors=TRUE)

n <- nrow(cell_data) # number of cells in cell_data
m <- nrow(cell_data_ad) # number of cells in cell_data_ad
A <- as.matrix(cell_data[, c('X1', 'X2')])
B <- as.matrix(cell_data_ad[, c('X1', 'X2')])
dist <- matrix(nrow=m, ncol=n)

for (i in 1:m){
  dist[i, ] <- sqrt(colSums((t(A) - B[i, ])^2))
}

nearest_neighbour_indices <- apply(dist, 1, which.min)
pred <- cell_data$CellType[nearest_neighbour_indices]

sink('cell_type_predicted, TANGYAO.txt')
cat(pred, sep='\n') # write entries of the vector, separated by newline characters
sink()