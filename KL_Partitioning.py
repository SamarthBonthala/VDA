# Kernighan Lin Algorithm for Circuit Partitioning
# Authors: Samarth Bonthala, Tarun Mittal

import math 
  
# Function to check 
# Log base 2 
def Log2(x): 
    return (math.log10(x) / math.log10(2)); 
  
# Function to check 
# if x is power of 2 
def isPowerOfTwo(n): 
    return (math.ceil(Log2(n)) == math.floor(Log2(n))); 


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
 	
def KL_Algo(adj_matrix,alp,n):

	n = n/2;

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

	no_ele_A = len(A)
	no_ele_B = len(B)
	temp_A = [0]* no_ele_A
	temp_B = [0]* no_ele_B
	
	# Intialize the matrix to 0
	adj_mat_A = [[0 for i in range(no_ele_A)] for j in range(no_ele_A)]
	adj_mat_B = [[0 for i in range(no_ele_B)] for j in range(no_ele_B)]
		
	# Adjacency matrix of partition A
	x = 0
	for i in A:
		#print(i)
		y = 0
		for j in A:
			#print(j)
			adj_mat_A[x][y] = adj_matrix[i][j]
			y = y + 1
		x = x + 1
					
	# Adjacency matrix of partition B
	x = 0
	for i in B:
		y = 0
		for j in B:
			adj_mat_B[x][y] = adj_matrix[i][j]
			y = y + 1
		x = x + 1
	
	alp_A = [ chr(i+97+alp[i]) for i in A ]
	alp_B = [ chr(i+97+alp[i]) for i in B ]
	
	print"parts"
	print(alp_A)
	print(alp_B)
	
	#print(A)
	#print(B)
		
	if(n>1):
		p_A1, p_B1, adj_A1, adj_B1 =  KL_Algo(adj_mat_A,A,n)
		p_A2, p_B2, adj_A2, adj_B2 =  KL_Algo(adj_mat_B,B,n)
			
 	return A,B,adj_mat_A,adj_mat_B
 	
def main():

	print ("Enter the name of the file where the adjacency matrix is stored")
	filename = raw_input("\n")
	print (filename)
	# Take input from the text file containing the adjacency matrix of unpartitioned graph
	adj_matrix = input_func(filename)
	
	# Enter number of partitions needed, n where n must be a power of 2
	
	print "Enter number of partitions needed (n has to be a power of 2): "
	n = int(raw_input("\n"))
	
	# Validation that the number of partitions is a power of 2
	#while(~isPowerOfTwo(n)):
		#print "Re-enter number of partitions. n has to be a power of 2."
		#n = int(raw_input("\n"))
	
	# Running the KL Algorithm
	no_of_nodes = len(adj_matrix[0])
	alp = [ i for i in range(no_of_nodes)]
	print(alp) 
	
	part_A,part_B,adj_mat_A,adj_mat_B = KL_Algo(adj_matrix,alp,n)
	
	# print "The two partitions are: \n"
	#print(part_A)
	#print(part_B)
	#print (adj_mat_A)
	#print (adj_mat_B)
	 
main()

