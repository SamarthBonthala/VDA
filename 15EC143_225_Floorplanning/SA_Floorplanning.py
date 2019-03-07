# Floorplanning algorithm employing Simulated Annealing and Stockmeyer's algorithm to compute minimum area and cost function based on area and wirelength (based on number of connections and center to center distance between blocks)

import random
import math
import os
from turtle import *
from Netlist_to_AdjMatrix import netlist_to_adj_mat
from draw_fp import shape
from stockmeyer import area_coord
from stockmeyer import vertical
from stockmeyer import horizontal

# Input Function
def input_func(filename):

	f = open(filename,'r')

	data = f.readlines()
	adj_matrix = []

	for i in data:
		temp = i.split()
		temp = [int(j) for j in temp]
		adj_matrix.append(temp)
  	
  	return adj_matrix

# Exchange two adjacent operands - Move Type 1
def move1(polish_exp):

	polish_exp_temp = polish_exp
	len_exp = len(polish_exp_temp)
		
	# To create operator and operand array seperately from the Polish expression
	operator = ['H','V']
	operators = []
	operands = []
	for i in polish_exp_temp:
		if i in operator:
			operators.append(i)
		else:
			operands.append(i)
	
	rand_no = random.randint(0,len(operands)-1)
	no1 = operands[rand_no]
	if (rand_no == len(operands)-1):
		no2 = operands[rand_no-1]
	else:
		no2 = operands[rand_no+1]
		
	for j in range(len_exp):
		if (polish_exp_temp[j] == no1):
			loc1 = j
		if (polish_exp_temp[j] == no2):
			loc2 = j	
			
	polish_exp_temp[loc1] = no2
	polish_exp_temp[loc2] = no1
			
	return polish_exp_temp

# Invert a chain formed by the operators
def move2(polish_exp):

	polish_exp_temp = polish_exp
	len_exp = len(polish_exp_temp)
		
	# To create operator and operand array seperately from the Polish expression
	operator = ['H','V']
	
	
def wirelength(adj_matrix, block_dimensions, node_no, node_coord):
	weight = 0
	n = len(adj_matrix[0])
	
	for i in range(n):

		x1 = node_coord[i][0] + (block_dimensions[node_no[i]][0])/2
		y1 = node_coord[i][1] + (block_dimensions[node_no[i]][1])/2

		for j in range(n):
			if(adj_matrix[i][j] !=0):
				x2 = node_coord[j][0] + (block_dimensions[node_no[j]][0])/2
				y2 = node_coord[j][1] + (block_dimensions[node_no[j]][1])/2

				dist = math.sqrt((x2-x1)**2 + (y2 - y1)**2)

				weight = weight + dist*adj_matrix[i][j]

	return weight
	
	
def annealing(adj_matrix, blocks, block_sizes):
	
	# Portion of code for initial temperature calculation
	# Idea: Run the algorithm for 4 times and compute difference in cutsize between the consecutive iterations
	# Compute average and back calculate and obtain the initial temperature
	
	A = X[:]
	B = Y[:]
	temp_part_A = A[:]
	temp_part_B = B[:]
	loop = 0
	init_temp_arr = []

	cost_func_factor = imbalance_calc(no_of_nodes)
	
	# Random number generation to shift to the alongside partition
	ele_arr = []
	for i in A:
		ele_arr.append(i)
	for i in B:
		ele_arr.append(i)
	length = len(ele_arr)
	
	while(loop < 4):
		x1 = random.randint(0, length-1)
		val = ele_arr[x1]
		if val in temp_part_A:
			temp_part_A.remove(val)
			temp_part_B.append(val)
		else:
			temp_part_B.remove(val)
			temp_part_A.append(val)

		cst, init_cutsize = cost_func(temp_part_A, temp_part_B, adj_matrix, cost_func_factor)
		init_temp_arr.append(cst)
		loop = loop + 1
		
	i = 0
	sum = 0
	while(i<3):
		sum = sum + abs(init_temp_arr[i+1] - init_temp_arr[i])
		i = i+1
		
	avg_cost = sum/3
	initial_temperature = -avg_cost/math.log(0.9)
		
	#print "Initial Temperature calculated:",initial_temperature
		
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

		x = random.randint(0, length-1)
		val1 = ele_arr[x]
		
		if val1 in A:
			A_temp.remove(val1)
			B_temp.append(val1)
		else:
			B_temp.remove(val1)
			A_temp.append(val1)

		cost_temp, cutsize_temp = cost_func(A_temp, B_temp, adj_matrix, cost_func_factor)
		# If solution is accepted and cost has decreased, choose the best option
		if(cost < best_cost):
			best_cost = cost
			best_part_A = A_temp[:]
			best_part_B = B_temp[:]
			
		delta_cost = cost_temp - cost

		#print "Delta_cost" + str(delta_cost)
		#print "Cutsize" + str(cutsize_temp)

		if(delta_cost <= 0): # Accept the soltuion when the cost decreases from previous iteration
			A = A_temp[:]
			B = B_temp[:]
			A_res = A
			B_res = B
			cost = cost_temp
			cutsize = cutsize_temp
			reject = 0
			temp_reject = 0
		elif ( math.exp(-(delta_cost/temperature)) > random.uniform(0,1)): # Accept the solution with a probability
			#print "tp" + str (math.exp(-(delta_cost/temperature))) + str(random.uniform(0,1))
			A = A_temp[:]
			B = B_temp[:]
			A_res = A
			B_res = B
			cost = cost_temp
			cutsize = cutsize_temp
			reject = 0
			temp_reject = 0
		else: # Increment reject counter and keep track of number of rejections 
			reject = reject + 1
			#print "Rejected Iteration" + str(reject)
			A_temp = A[:]
			B_temp = B[:]
			if(reject >= 5): # If number of rejections for a particular temperature is greater than 5, go to next temperature
				temp_reject = temp_reject + 1
				temperature = temperature*math.pow(tempfact,temp_iteration) 
				temp_iteration = temp_iteration + 1 # Update the temperature iteration
				if(temp_iteration>5): # Terminate the algorithm once 5 temperatures have been rejected
					temp_reject = 10
				#print "Rejected_Temperature: " + str(temp_reject)


	return best_part_A,best_part_B,best_cost
	
	
def main():

	print ("Enter the name of the file containing the required netlist")
	filename = raw_input("\n")
	
	# Converting the netlist to adjacency matrix
	nodes = netlist_to_adj_mat(filename)
	
	# Take input from the text file containing the adjacency matrix of unpartitioned graph
	adj_matrix = input_func("inp_adj_mat.txt")
	
	# Look up table for storing the block dimensions in the form of a dictionary
	block_dim = dict()
	block_dim.update({'DFF': [4,2]})
	block_dim.update({'NOT': [1,1]})
	block_dim.update({'AND': [3,3]})
	block_dim.update({'NAND': [2,3]}) 
	block_dim.update({'NOR': [2,3]})
	block_dim.update({'OR': [3,3]})

	blocks = range(1,len(nodes)+1) # Blocks labelled as 1,2,3,4,....,(total_no)
	block_sizes = [0]*len(blocks)
	# Computation of the block sizes on comparision with the entries in the look up table
	j = 0
	for i in nodes:
		block_sizes[j] = block_dim[i]
		j = j+1
	polish_exp_temp = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H']
	print polish_exp_temp
	x = move1(polish_exp_temp)
	print x
		
	# Run simulated annealing algorithm for obtaining the optimal floorplan
	#best_polish_exp, best_area, best_coord, block_dim = annealing(adj_matrix, blocks, block_sizes)
	
	wn = Screen()
	sarah = Turtle()
	wn.setworldcoordinates(0, 0, 50, 50)
	sarah.speed(0)

	#node_type = [0,1,2,3,4]

	#block_dimensions = [[9,6],[6,8],[3,6],[3,7],[6,5]]

	#node_coord = [[0,0],[9,0],[0,6],[3,6],[6,8]]


	for i in range(len(node_type)):
		shape(str(i),best_coord[i][0],best_coord[i][1],block_dim[node_type[i]][0],block_dim[node_type[i]][1],sarah)

	wn.exitonclick()
	
main()	
	
