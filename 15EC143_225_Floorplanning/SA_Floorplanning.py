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
	operand = range(1,len_exp+1)
	chains = []
	location = []
	i = 0
	temp_arr = []
	while(i<len_exp):
		
		if(polish_exp_temp[i] in operator):
			temp_arr.append(polish_exp_temp[i])
			location.append(i)
		j = i+1

		while(j<(len_exp-1)):
			if(polish_exp_temp[j] in operator):
				temp_arr.append(polish_exp_temp[j])
			elif(polish_exp_temp[j] in operand):
				chains.append(temp_arr)
				temp_arr = []
				i = j+1
			j = j+1
		i = i+1


def move3(polish_exp):
	polish_exp_temp = polish_exp
	len_exp = len(polish_exp_temp)

	operator = ['H','V']
	operand = range(1,len_exp+1)
	adjacent = []
	location = []

	for i in range(len_exp-1):
		temp_arr = []
		if((polish_exp_temp[i] in operator and polish_exp_temp[i+1] in operand) or (polish_exp_temp[i] in operand and polish_exp_temp[i+1] in operator)):
			temp_arr.append(polish_exp_temp[i])
			temp_arr.append(polish_exp_temp[i+1])
			adjacent.append(temp_arr)
			location.append(i)
	len_adj = len(adjacent)
	rand_no = random.randint(0,len(adjacent))

	swap = adjacent[rand_no]
	swap_loc = location[rand_no]

	temp = polish_exp_temp[swap_loc]
	polish_exp_temp[swap_loc] = polish_exp_temp[swap_loc + 1]
	polish_exp_temp[swap_loc + 1] = temp

	if(balloting_prop(polish_exp_temp) == 0):
		move3(polish_exp_temp)

	return polish_exp_temp

def balloting_prop(polish_exp):


	
	
def wirelength(adj_matrix, block_dimensions, block_coord):
	weight = 0
	n = len(adj_matrix[0])
	#node_no = range(0,n)
	
	for i in range(n):

		x1 = node_coord[i][0] + (block_dimensions[i][0])/2
		y1 = node_coord[i][1] + (block_dimensions[i][1])/2

		for j in range(n):
			if(adj_matrix[i][j] !=0):
				x2 = node_coord[j][0] + (block_dimensions[j][0])/2
				y2 = node_coord[j][1] + (block_dimensions[j][1])/2

				dist = math.sqrt((x2-x1)**2 + (y2 - y1)**2)

				weight = weight + dist*adj_matrix[i][j]

	return weight

def cost_func_param(adj_matrix):
	cost_parm = 0.9
	return cost_param

def cost_func(polish_expression, block_dimensions, adj_matrix):
	# Cost = Area + cost_func_factor*wirelength
	area, block_coord, size = area_coord(polish_expression, block_dimensions)

	wirelen = wirelength(adj_matrix, block_dimensions, block_coord)

	cost_param = cost_func_param(adj_matrix)

	cost = area + cost_param*wirelen

	return cost,size
	
def annealing(adj_matrix, blocks, block_dimensions):
	
	# Portion of code for initial temperature calculation
	# Idea: Run the algorithm for 4 times and compute difference in cost between the consecutive iterations
	# Compute average and back calculate and obtain the initial temperature

	node_list_size = len(adj_matrix[0])
	len_pol_exp = 2*node_list_size - 1
	polish_expression = []
	
	# Initial polish expression
	j = 0
	for i in range(len_pol_exp):
		if (i%2 == 0 and i != 0 and i != 1):
			polish_expression.append('V')
		elif (i == 0 or i == 1):
			polish_expression.append(i+1)
			j = 3
		else:
			polish_expression.append(j)
			j = j+1
	 
	# polish_expression has the required [1,2,'V',3,'V',....]
	pol_exp_temp = polish_expression # For computation of initial temperature

	while(loop < 5):
		move_no = random.randint(1, 4) # Generate a random number from 1 to 3 to select the type of move
		if(move_no == 1):
			pol_exp_temp = move1(pol_exp_temp)
		elif (move_no == 2):
			pol_exp_temp = move2(pol_exp_temp)
		else:
			pol_exp_temp = move3(pol_exp_temp)

		cst, size = cost_func(pol_exp_temp, block_dimensions, adj_matrix)
		init_temp_arr.append(cst) # Appends the cost obtained in every iteration into array
		loop = loop + 1
		
	i = 0
	sum = 0
	while(i<4):
		sum = sum + abs(init_temp_arr[i+1] - init_temp_arr[i])
		i = i+1
		
	avg_cost = sum/4
	initial_temperature = -avg_cost/math.log(0.9)
		
	print "Initial Temperature calculated:",initial_temperature
	
	# Annealing algorithm begins here

	tempfact = 0.85 # r value in (r^i)*T to constantly decrease temperature after old temperature is rejected
	temperature = 1 # T value
	temp_iteration = 1 # iteration number
	
	polish_exp = polish_expression # Initial expression (at t=0)
	polish_exp_temp = []
	reject = 0
	temp_reject = 0
	
	cost, size = cost_func(polish_exp, block_dimensions) # Initial cost (at t=0)
	cost_temp = 0
	size_temp = 0
	# Keeping track of the best solution obtained so far - Global minima
	best_polish_exp = polish_exp_temp
	best_area,best_coord, best_size = area_coord(polish_exp_temp, block_dimensions)
	
	# Starting the annealing process 
	
	#while(temp_reject<5):
	while(temperature > 0.5):

		x = random.randint(1,4)
		
		if(move_no == 1):
			polish_exp_temp = move1(polish_exp)
		elif (move_no == 2):
			polish_exp_temp = move2(polish_exp)
		else:
			polish_exp_temp = move3(polish_exp)

		cost_temp, size_temp = cost_func(polish_exp_temp, block_dimensions)
		# If solution is accepted and cost has decreased, choose the best option
		if(cost < best_cost):
			best_cost = cost
			best_size = size
			best_polish_exp = polish_exp
			best_area,best_coord = area_coord(best_polish_exp, block_dimensions)
			
		delta_cost = cost_temp - cost

		#print "Delta_cost" + str(delta_cost)
		#print "Cutsize" + str(cutsize_temp)

		if(delta_cost <= 0): # Accept the solution if the cost decreases from previous iteration
			cost = cost_temp
			size = size_temp
			polish_exp = polish_exp_temp
			reject = 0
			temp_reject = 0
		elif (math.exp(-(delta_cost/temperature)) > random.uniform(0,1)): # Accept the solution with a probability
			cost = cost_temp
			size = size_temp
			polish_exp = polish_exp_temp
			reject = 0
			temp_reject = 0
		else: # Increment reject counter and keep track of number of rejections 
			reject = reject + 1
			#print "Rejected Iteration" + str(reject)
			if(reject >= 5): # If number of rejections for a particular temperature is greater than 5, go to next temperature
				temp_reject = temp_reject + 1
				temperature = temperature*math.pow(tempfact,temp_iteration) 
				temp_iteration = temp_iteration + 1 # Update the temperature iteration
				#if(temp_iteration>5): # Terminate the algorithm once 5 temperatures have been rejected
				#	temp_reject = 10
				#print "Rejected_Temperature: " + str(temp_reject)


	return best_polish_exp, best_area, best_coord, best_size
	
	
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

	block_names = range(1,len(nodes)+1) # Blocks labelled as 1,2,3,4,....,(total_no)
	block_dimensions = [0]*len(blocks)
	# Computation of the block sizes on comparision with the entries in the look up table
	j = 0
	for i in nodes:
		block_dimensions[j] = block_dim[i]
		j = j+1
	polish_exp_temp = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H']
	print polish_exp_temp
	x = move1(polish_exp_temp)
	print x
		
	# Run simulated annealing algorithm for obtaining the optimal floorplan
	best_polish_exp, best_area, best_coord, best_size = annealing(adj_matrix, block_names, block_dimensions)
	
	wn = Screen()
	sarah = Turtle()
	wn.setworldcoordinates(0, 0, best_size[1][0]+5,best_size[1][1]+5)
	sarah.speed(0)

	for i in range(len(block_sizes)):
		shape(str(i+1),best_coord[i][0],best_coord[i][1],block_dimensions[i][0],block_dimensions[i][1],sarah)

	wn.exitonclick()

main()