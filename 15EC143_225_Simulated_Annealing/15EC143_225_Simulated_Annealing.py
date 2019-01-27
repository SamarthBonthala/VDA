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
	
def cost_func(A, B):

def Sim_Ann(adj_matrix,n):
	
	# Split into two equal partitions randomly
	A = []
	B = []
	
	no_of_nodes = len(adj_matrix[0])
	
	for i in range(no_of_nodes):
		if (i < no_of_nodes/2):
			A.append(i)
		else:
			B.append(i)
			
	
	
	
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
		
	# Running the KL Algorithm recursively
	no_of_nodes = len(adj_matrix[0])
	alp = [ i for i in range(no_of_nodes)]
	
	if (n == 1):
		print alp
		return
		
	print "Partitions are as follows:"
	Sim_Ann(adj_matrix,n)
	
	 
main()

