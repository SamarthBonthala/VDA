# Simulated Annealing Algorithm for Circuit/Graph Partitioning
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

# Computing the cost function
# f = C + lambda*(Imbalance)
# C = cutsize (sum of edge weights of all the crossover edges from A to B)
# Imbalance = (no_of_nodes_A - no_of_nodes_B)^2
# Returns cost and cutsize
	
def cost_func(A, B, adj_matrix, cost_func_factor):

	cutsize = 0

	for i in A:
		for j in B:
			cutsize = cutsize + adj_matrix[i][j]

	lenA = len(A)
	lenB = len(B)

	imbalance_fact = (lenA - lenB)**2

	cost = cutsize + cost_func_factor*imbalance_fact

	return cost,cutsize

# Function for Simulated Annealing Algorithm
# Heuristic Algorithm for Partitioning
# Inputs: adj_matrix and number of partitions needed, n

def Sim_Ann(adj_matrix,n):
	
	#n = n/2
	# Spl[it into two equal partitions randomly
	A = []
	B = []
	cost_func_factor = 0.5 # Related to the cost function
	
	no_of_nodes = len(adj_matrix[0])
	
	for i in range(no_of_nodes):
		if (i < no_of_nodes/2):
			A.append(i)
		else:
			B.append(i)
		
	# Portion of code for initial temperature calculation
	# Idea: Run the algorithm for 4 times and compute difference in cutsize between the consecutive iterations
	# Compute average and back calculate and obtain the initial temperature
	
	temp_part_A = A[:]
	temp_part_B = B[:]
	loop = 0
	init_temp_arr = []

	while(loop < 4):
		x1 = random.randint(0, no_of_nodes-1)
		if x1 in temp_part_A:
			temp_part_A.remove(x1)
			temp_part_B.append(x1)
		else:
			temp_part_B.remove(x1)
			temp_part_A.append(x1)

		cst, init_cutsize = cost_func(temp_part_A, temp_part_B, adj_matrix, cost_func_factor)
		init_temp_arr.append(init_cutsize)
		loop = loop + 1
		
	i = 0
	sum = 0
	while(i<3):
		sum = sum + abs(init_temp_arr[i+1] - init_temp_arr[i])
		i = i+1
		
	avg_cost = sum/3
	initial_temperature = -avg_cost/math.log(0.9)
		
	print "Initial Temperature (chosen for calculation):",initial_temperature
		
	tempfact = 0.85 # r value in (r^i)*T
	temperature = 1 # T value
	temp_iteration = 1 # iteration number
	
	A_temp = A
	B_temp = B
	
	A_res = A_temp
	B_res = B_temp

	cost, cutsize = cost_func(A, B, adj_matrix, cost_func_factor)
	cost_temp = 0
	cutsize_temp = 0

	reject = 0
	temp_reject = 0
	
	# Keeping track of the best solution obtained so far - Global minima
	best_part_A = A[:]
	best_part_B = B[:]
	best_cost = cost
	
	# Starting the iterations
	
	while(temp_reject<5):
		print "new"

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
		# If solution is accepted and cost has decreased, choose the best option
		if(cost < best_cost):
			best_cost = cost
			best_part_A = A_temp[:]
			best_part_B = B_temp[:]
			
		delta_cost = cost_temp - cost

		print "Delta_cost" + str(delta_cost)
		print "Cutsize" + str(cutsize_temp)

		if(delta_cost <= 0): # Accept the soltuion when the cost decreases from previous iteration
			A = A_temp[:]
			B = B_temp[:]
			A_res = A
			B_res = B
			cost = cost_temp
			cutsize = cutsize_temp
			reject = 0
			temp_reject = 0
			# print"1"
		elif ( math.exp(-(delta_cost/temperature)) > random.uniform(0,1)): # Accept the solution with a probability
			print "tp" + str (math.exp(-(delta_cost/temperature))) + str(random.uniform(0,1))
			A = A_temp[:]
			B = B_temp[:]
			A_res = A
			B_res = B
			cost = cost_temp
			cutsize = cutsize_temp
			reject = 0
			temp_reject = 0
			#print "2"
		else: # Increment reject counter and keep track of number of rejections 
			reject = reject + 1
			print "Rejected Iteration" + str(reject)
			A_temp = A[:]
			B_temp = B[:]
			if(reject >= 5): # If number of rejections for a particular temperature is greater than 5, go to next temperature
				temp_reject = temp_reject + 1
				temperature = temperature*math.pow(tempfact,temp_iteration) 
				temp_iteration = temp_iteration + 1 # Update the temperature iteration
				if(temp_iteration>5): # Terminate the algorithm once 5 temperatures have been rejected
					temp_reject = 10
				print "Rejected_Temperature: " + str(temp_reject)

		print(A)
		print(B)
		print(A_res)
		print(B_res)

	return best_part_A,best_part_B,best_cost
	
	
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
		
	
	A,B,cost = Sim_Ann(adj_matrix,n)
	print "\n Best Partition until now is as follows and accepted:"
	print "Partition A:", A
	print "Partition B:", B
	print "Least cost:",cost
		 
main()

