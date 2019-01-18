# Kernighan Lin Algorithm for Circuit Partitioning
# Authors: Samarth Bonthala, Tarun Mittal

# Global Variables


# Input Function
def input_func(filename):

	f = open(filename,'r')

	data = f.readlines()
	adj_matrix = []

	for i in data:
		temp = i.split()
		temp = [int(j) for j in temp]
		adj_matrix.append(temp)
  	
  	return adj_matrix;
	# print (adj_matrix)
	
# Function for the KL algorithm
# Inputs: Adjacency matrix
# Returns: Two partitions with minimum cut cost
# For n partitions, run the partitioning multiple times
 	
def KL_Algo(adj_matrix):

	dummy = 0 # To trace if a dummy node was added during partitioning or not
	no_of_nodes = len(adj_matrix[0])

	# Adding a dummy node

	if (len(adj_matrix[0])%2 != 0):
		no_of_nodes = no_of_nodes + 1
		dummy = 1
	
		for i in range(no_of_nodes-1):
			adj_matrix[i].append(0)
		temp = [0]*(no_of_nodes)
		adj_matrix.append(temp)
			
	# Random partitioning to form a bipartition
		 
	locked = [0]*len(adj_matrix[0]) # To indicate if node is in locked state or not
	A = []
	B = []

	for i in range(len(locked)):
		if(i<(len(locked)/2)):
			A.append(i)
	  	else:
	  		B.append(i)

	print(A)
	print(B)

	# Computation of D, D(i) = E(i) - I(i) where i represents each node
	
	D = [0]*no_of_nodes
	for i in range(no_of_nodes):
	
		if i in A:
	
			for j in range(no_of_nodes):
	
				if j in A:
					D[i] = D[i] - adj_matrix[i][j]
				else:
					D[i] = D[i] + adj_matrix[i][j]
		else:
			for j in range(no_of_nodes):
	
				if j in B:
					D[i] = D[i] - adj_matrix[i][j]
				else:
					D[i] = D[i] + adj_matrix[i][j]
		
	print(D)

	# Calculation of g - Gains
		
	max_g = 100 
	while( max_g > 0 ): # Run the algorithm until the max gain becomes 0 or less than 0 

		g = [[0 for i in range(no_of_nodes)] for j in range(no_of_nodes)]
		max_g = 0
		max_i = -1
		max_j = -1
		for i in A:
			if (locked[i] ==0):
				for j in B:
					if(locked[j] == 0):
				
						g[i][j] = D[i]+D[j]-2*adj_matrix[i][j]
						if(g[i][j] > max_g):
							max_g = g[i][j]
							max_i = i
							max_j = j

		print (g)
		print(max_g)
		print(max_i)
		print(max_j)

		if(max_g>0):
			locked[max_i] = 1
			locked[max_j] = 1
			A.remove(max_i)
			B.remove(max_j)
			A.append(max_j)
			B.append(max_i)
	
		for i in range(no_of_nodes):
		
			if(locked[i] == 0):
			
				if i in A:
					x = 1
				else:
					x = -1
				
				D[i] = D[i] + 2*x*(adj_matrix[i][max_i] - adj_matrix[i][max_j])
			
		print(D)

	# Removal of Dummy node

	if (dummy == 1):
		temp = no_of_nodes - 1
		if temp in A:
			A.remove(temp)
		if temp in B:
			B.remove(temp)
	
	#print(A)
	#print(B)
 	
 	return A,B
 	
def main():

	print ("Enter the name of the file where the adjacency matrix is stored")
	filename = raw_input("\n")
	print (filename)
	# Take input from the text file containing the adjacency matrix of unpartitioned graph
	adj_matrix = input_func(filename)
	
	# Running the KL Algorithm
	part_A,part_B = KL_Algo(adj_matrix)
	
	print "The two partitions are: \n"
	print(part_A)
	print(part_B)
	
main()

