# Kernighan Lin Algorithm for Circuit Partitioning
# Authors: Samarth Bonthala, Tarun Mittal
  
import random
import math

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
	
def cost_func(A, B, adj_matrix, cost_func_factor):

	cutsize = 0

	for i in A:
		for j in B:

			cutsize = cutsize + adj_matrix[i][j]

	lenA = len(A)
	lenB = len(B)

	imbalance_fact = (lenA - lenB)**2

	cost = cutsize + cost_func_factor*imbalance_fact

	#print (cost)

	return cost,cutsize

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
			
	tempfact = 0.85
	temperature = 1
	temp_iteration = 1
	cost_func_factor = 0.5
	A_temp = []
	B_temp = []
	for i in range(no_of_nodes):
		if (i < no_of_nodes/2):
			A_temp.append(i)
		else:
			B_temp.append(i)
	
	cost, cutsize = cost_func(A, B, adj_matrix, cost_func_factor)
	cost_temp = cost
	cutsize_temp = cutsize

	reject = 0
	temp_reject = 0

	while(temp_reject<5):
		print"new"

		x = random.randint(0, no_of_nodes-1)
		print(x)
		print(A)
		print(B)
		if x in A:
			A_temp.remove(x)
			B_temp.append(x)
		else:
			B_temp.remove(x)
			A_temp.append(x)

		print(A_temp)
		print(B_temp)
		cost_temp, cutsize_temp = cost_func(A_temp, B_temp, adj_matrix, cost_func_factor)

		delta_cost = cost_temp - cost

		print "delta_cost" + str(delta_cost)
		print "cutsize" + str(cutsize_temp)

		if(delta_cost <= 0):
			A = A_temp
			B = B_temp
			cost = cost_temp
			cutsize = cutsize_temp
			reject = 0
			temp_reject = 0
			print"1"

		elif ( math.exp(-(delta_cost/temperature)) > random.uniform(0,1)):
			print "tp" + str (math.exp(-(delta_cost/temperature))) + str(random.uniform(0,1))
			A = A_temp
			B = B_temp
			cost = cost_temp
			cutsize = cutsize_temp
			reject = 0
			temp_reject = 0
			print"2"
		else:
			reject = reject + 1
			print "rejected" + str(reject)
			A_temp = A
			B_temp = B
			if(reject >= 5):
				temp_reject = temp_reject + 1
				temperature = temperature*math.pow(tempfact,i) 
				temp_iteration = temp_iteration + 1
				if(temp_iteration>5):
					temp_reject = 10
				print "rejectedtemp" + str(temp_reject)

		print(A)
		print(B)



	return A,B, cutsize
	
	
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
		
	
	A,B, cutsize = Sim_Ann(adj_matrix,n)
	print "Partitions are as follows:"
	print(A)
	print(B)
	print(cutsize)
	
	 
main()

