# Kernighan Lin Algorithm for Circuit Partitioning
# Authors: Samarth Bonthala, Tarun Mittal
  
# Function to check if n is a power of 2 or not
def isPowerOfTwo(n): 
    if (n == 0): 
        return False
    while (n != 1): 
            if (n % 2 != 0): 
                return False
            n = n // 2
              
    return True
    
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
# Inputs: Adjacency matrix, Number of elements and Node names
# Output: Two partitions with minimum cut cost
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
                #alp.append(25+97)
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

	# Removal of Dummy node

	if (dummy == 1):
		temp = no_of_nodes - 1
		if temp in A:
			A.remove(temp)
		if temp in B:
			B.remove(temp)

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
        
        #print"A,B,alp"
        #print(A)
        #print(B)

        #print(alp)
	alp_A = [ chr(97+alp[A[i]]) for i in range(len(A)) ]
	alp_B = [ chr(97+alp[B[i]]) for i in range(len(B)) ]
	
	
	if(n<2):
		print(alp_A)
		print(alp_B)
		
	if(n>1):
		p_A1, p_B1, adj_A1, adj_B1 =  KL_Algo(adj_mat_A,A,n)
		p_A2, p_B2, adj_A2, adj_B2 =  KL_Algo(adj_mat_B,B,n)
			
 	return A,B,adj_mat_A,adj_mat_B
 	
def main():

	print ("Enter the name of the file where the adjacency matrix is stored")
	filename = raw_input("\n")

	# Take input from the text file containing the adjacency matrix of unpartitioned graph
	adj_matrix = input_func(filename)
	
	# When there is only on entry in the adjacency matrix
	if (len(adj_matrix) == 1):
		print "Only one node is present, partitioning not possible"
		return
		
	# Enter number of partitions needed, n where n must be a power of 2
	
	print "Enter number of partitions needed (n has to be a power of 2): "
	n = int(raw_input("\n"))
	
	if (isPowerOfTwo(n) == 0):
		print "Number of partitions entered is not a power of 2 and therefore partitioning not possible."
		
	while(isPowerOfTwo(n) != 1):
		n = int(raw_input("Re-enter value of n such that n is a power of 2. \n"))
			
	# Tackling corner cases
		
	# When number of partitions required are greater than number of nodes
	if (n > len(adj_matrix[0])):
		print "Number of nodes are less than partitions required. Partitioning not possible"
		return
		
	# Running the KL Algorithm
	no_of_nodes = len(adj_matrix[0])
	alp = [ i for i in range(no_of_nodes)]
	
	print "Partitions are as follows:"
	part_A,part_B,adj_mat_A,adj_mat_B = KL_Algo(adj_matrix,alp,n)
	
	 
main()

