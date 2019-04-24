# Floorplanning algorithm employing Simulated Annealing and Stockmeyer's algorithm to compute minimum area and cost function based on area and wirelength (based on number of connections and center to center distance between blocks)

import random
import math
import os
import time
from turtle import *
from Netlist_to_AdjMatrix import netlist_to_adj_mat
from stockmeyer import area_coord
from stockmeyer import vertical
from stockmeyer import horizontal
import numpy as np

def shape(label,x,y,a,b,sarah):
	sarah.goto(x,y)
	sarah.fillcolor("yellow")
	sarah.pendown()
	sarah.begin_fill()
	sarah.forward(a)
	sarah.left(90)
	sarah.forward(b)
	sarah.left(90)
	sarah.forward(a)
	sarah.left(90)
	sarah.forward(b)
	sarah.left(90)
	sarah.end_fill()
	sarah.penup()
	sarah.goto((x+a/2.0),(y+b/2.0))
	sarah.write(label, False, align="center")

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

	polish_exp_temp = polish_exp[:]
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
	
	# print("len of operands", len(operands))
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

	polish_exp_temp = polish_exp[:]
	len_exp = len(polish_exp_temp)
	len_chain = []
	loc = []
	i = 0

	# print("pol_exp_temp", polish_exp_temp)
	while(i<len(polish_exp_temp)):

		if(polish_exp_temp[i] == 'V' or polish_exp_temp[i] == 'H' ):
			loc.append(i)
			len_chain.append(1)
			i = i +1
			# print("loc", loc)

			if(i == len(polish_exp_temp) ):
				break
			while(polish_exp_temp[i] == 'V' or polish_exp_temp[i] == 'H' ):
				len_chain[len(loc) - 1] = len_chain[len(loc) - 1] + 1
				i = i + 1
				if(i == len(polish_exp_temp) ):
					break

		else:
			i = i + 1

	len_loc = len(loc)
	rand_loc = 0

	if(len_loc>1):
		rand_loc = random.randint(0, len_loc-1)

	# print("loc", loc)
	# print("rand_loc", rand_loc)

	i = loc[rand_loc]
	while (i < (loc[rand_loc] + len_chain[rand_loc] )):
		if(polish_exp_temp[i] == 'V'):
			polish_exp_temp[i] = 'H'
		elif(polish_exp_temp[i] == 'H'):
			polish_exp_temp[i] = 'V'
		i = i + 1

	return polish_exp_temp


def move3(polish_exp):
	polish_exp_temp = polish_exp[:]
	len_exp = len(polish_exp_temp)

	operator = ['H','V']
	operand = range(1,len_exp+1)
	adjacent = []
	location = []

	# print("polish_exp", polish_exp)
	for i in range(len_exp-1):
		temp_arr = []
		if(polish_exp_temp[i] in operator and polish_exp_temp[i+1] in operand):
			temp_arr.append(polish_exp_temp[i])
			temp_arr.append(polish_exp_temp[i+1])
			adjacent.append(temp_arr)
			location.append(i)
		elif(polish_exp_temp[i] in operand and polish_exp_temp[i+1] in operator):
			temp_arr.append(polish_exp_temp[i])
			temp_arr.append(polish_exp_temp[i+1])
			adjacent.append(temp_arr)
			location.append(i)

	# print("adjacent", adjacent)
	len_adj = len(adjacent)
	rand_no = 0
	if(len_adj>1):
		rand_no = random.randint(0,len(adjacent)-1)

	swap = adjacent[rand_no]
	swap_loc = location[rand_no]

	temp = polish_exp_temp[swap_loc]
	polish_exp_temp[swap_loc] = polish_exp_temp[swap_loc + 1]
	polish_exp_temp[swap_loc + 1] = temp

	return polish_exp_temp,swap_loc

def balloting_prop(polish_exp,swap_loc):

	operator = ['H','V']
	alp_count = 0
	num_count = 0
	i = 0
	flag = 0
	while(i < len(polish_exp)):
		if polish_exp[i] in operator:
			alp_count = alp_count + 1
		else:
			num_count = num_count + 1

		if (alp_count < num_count):
			i = i+1
		else:
			flag = 1
			# print("flagggggg")

			return 1

	if (flag == 1):
		return 1
	return 0

def move(polish_expression):

	# print("polish_expression" , polish_expression)
	polish_exp_temp = polish_expression[:]

	move_no = random.randint(1,3)
	#move_no = 2

	if(move_no == 1):
		polish_exp_temp1 = move1(polish_exp_temp)
	elif (move_no == 2):
		polish_exp_temp1 = move2(polish_exp_temp)
	else:
		polish_exp_temp1, swap_loc = move3(polish_exp_temp)
		while (balloting_prop(polish_exp_temp1,swap_loc) == 1):
			polish_exp_temp1, move_no = move3(polish_exp_temp)

	return polish_exp_temp1, move_no

def wirelength(adj_matrix, block_dimensions, node_coord):
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
	cost_param = 0.5
	return cost_param

def cost_func(polish_expression, block_dimensions, adj_matrix):
	# Cost = Area + cost_func_factor*wirelength
	area, block_coord, size = area_coord(polish_expression[:], block_dimensions)

	wirelen = wirelength(adj_matrix, block_dimensions, block_coord)

	cost_param = cost_func_param(adj_matrix)

	# print("area", area)
	# print("wirelen", wirelen)
	# print("size", (size[1] - size[0])*(size[1] - size[0]))

	cost = 12*area + cost_param*wirelen + 1.2*(size[1] - size[0])*(size[1] - size[0])

	return cost,size, area, block_coord


	
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

	#print("initial polish_exp", polish_expression)
	 
	# polish_expression has the required [1,2,'V',3,'V',....]
	pol_exp_temp = polish_expression[:] # For computation of initial temperature
	loop = 0
	init_temp_arr = []
	cost_temp = 0
	size_temp = 0
	best_size = 0
	coord_temp = []

	while(loop < 5):

		# Choose move using the move function and the move function returns the polish expression after moving
		pol_exp_temp, move_no = move(pol_exp_temp)
		# print("pol_exp_temp" ,pol_exp_temp)
		# print("move_no", move_no)
		# move_no = random.randint(1, 3) # Generate a random number from 1 to 3 to select the type of move
		# if(move_no == 1):
		# 	pol_exp_temp = move1(pol_exp_temp)
		# elif (move_no == 2):
		# 	pol_exp_temp = move2(pol_exp_temp)
		# else:
		# 	pol_exp_temp1, swap_loc = move3(pol_exp_temp)
		# 	while(balloting_prop(pol_exp_temp1, swap_loc) == 0):
		# 		pol_exp_temp1, swap_loc = move3(pol_exp_temp)
		# 	pol_exp_temp = pol_exp_temp1

		cst, size, area_temp, coord_temp = cost_func(pol_exp_temp, block_dimensions, adj_matrix)
		init_temp_arr.append(cst) # Appends the cost obtained in every iteration into array
		loop = loop + 1
		
	i = 0
	sum = 0
	while(i<4):
		sum = sum + abs(init_temp_arr[i+1] - init_temp_arr[i])
		i = i+1
		
	avg_cost = sum/4
	initial_temperature = -avg_cost/math.log(0.9)
		
	print ("Initial Temperature calculated:",initial_temperature)
	
	# Annealing algorithm begins here

	tempfact = 0.85 # r value in (r^i)*T to constantly decrease temperature after old temperature is rejected
	temperature = initial_temperature # T value
	temp_iteration = 1 # iteration number
	
	polish_exp = polish_expression[:] # Initial expression (at t=0)
	polish_exp_temp = polish_exp[:]
	reject = 0
	temp_reject = 0
	
	cost, size, best_area, best_coord  = cost_func(polish_exp, block_dimensions,adj_matrix) # Initial cost (at t=0)
	cost_temp = 0
	size_temp = 0
	best_size = size
	best_cost = cost 
	# Keeping track of the best solution obtained so far - Global minima
	best_polish_exp = polish_exp_temp[:]
	#best_area,best_coord, best_size = area_coord(polish_exp_temp, block_dimensions)
	N = len(adj_matrix[0])
	no_of_moves = 0
	uphill  = 0
	# Starting the annealing process 
	
	#while(temp_reject<5):
	timeout = time.time() + 3600
	while(temperature > (initial_temperature/10000) and time.time()<timeout): # Until the temperature reaches 0.5, keep iterating

		# Choose move using the move function and the move function returns the polish expression after moving
		polish_exp_temp , move_no = move(polish_exp_temp)
		no_of_moves = no_of_moves + 1

		# print("polish_exp_temp", polish_exp_temp)
		# print("move_no", move_no)

		cost_temp, size_temp, area_temp, coord_temp = cost_func(polish_exp_temp, block_dimensions,adj_matrix)
		# print("coord_temp", coord_temp)
		# If solution is accepted and cost has decreased, choose the best option
		if(cost < best_cost):
			best_cost = cost
			best_size = size
			best_polish_exp = polish_exp[:]
			#best_area,best_coord,best_size = area_coord(best_polish_exp, block_dimensions)
			best_area = area_temp
			best_coord = coord_temp[:]

		delta_cost = cost_temp - cost

		#print "Delta_cost" + str(delta_cost)
		#print "Cutsize" + str(cutsize_temp)

		if(delta_cost <= 0): # Accept the solution if the cost decreases from previous iteration
			cost = cost_temp
			size = size_temp
			polish_exp = polish_exp_temp[:]
			reject = 0
			temp_reject = 0
		elif (math.exp(-(delta_cost/temperature)) > random.uniform(0,1)): # Accept the solution with a probability
			cost = cost_temp
			size = size_temp
			polish_exp = polish_exp_temp[:]
			reject = 0
			temp_reject = 0
			uphill = uphill + 1
		else: # Increment reject counter and keep track of number of rejections 
			reject = reject + 1
			#print "Rejected Iteration" + str(reject)
		if(uphill > N or no_of_moves>2*N): # If number of rejections for a particular temperature is greater than k*no_of_blocks, go to next temperature
				
			uphill = 0
			no_of_moves = 0
			temp_reject = temp_reject + 1
			temperature = temperature*math.pow(tempfact,temp_iteration) 
			print("new temp ", temperature)
			temp_iteration = temp_iteration + 1 # Update the temperature iteration


	# print("initial_temperature", initial_temperature)

	return best_polish_exp, best_area, best_coord, best_size

def grid(x,y,sarah):
	A = list(np.linspace(0,x,x*2+1))
	B = list(np.linspace(0,y,y*2+1))
	print A
	print B
	# xcorrec = x
	# ycorrec = y
	# correc_flag = 0
	# # Correction if we get multiples of 0.5 as value as we are multiplying the node_coord by 1.5 as well as the area too
	# if((x*2)%2 != 0 or (y*2)%2 !=0):
	# 	correc_flag = 1
	# 	xcorrec = x*2+1
	# 	ycorrec = y*2+1
	# 	A = list(np.linspace(0,x,xcorrec))
	# 	B = list(np.linspace(0,y,ycorrec))

	for i in A:

		sarah.goto(i,0)
		sarah.pencolor("red")
		sarah.pendown()
		sarah.left(90)
		sarah.forward(y)
		sarah.penup()
		sarah.right(90)

	for j in B:

		sarah.goto(0,j)
		sarah.pencolor("blue")
		sarah.pendown()
		sarah.forward(x)
		sarah.penup()

	# return A,B,xcorrec,ycorrec,correc_flag

def main():

	print ("Enter the name of the file containing the required netlist")
	filename = raw_input("\n")
	
	# Converting the netlist to adjacency matrix
	nodes = netlist_to_adj_mat(filename)
	
	# Take input from the text file containing the adjacency matrix of unpartitioned graph
	adj_matrix = input_func("inp_adj_mat.txt")
	
	# Look up table for storing the block dimensions in the form of a dictionary
	block_dim = dict()
	block_dim.update({'DFF': [8,5]})
	block_dim.update({'NOT': [2,1]})
	block_dim.update({'AND': [4,3]})
	block_dim.update({'NAND': [2,3]}) 
	block_dim.update({'NOR': [2,3]})
	block_dim.update({'OR': [4,3]})

	block_names = range(1,len(nodes)+1) # Blocks labelled as 1,2,3,4,....,(total_no)
	block_dimensions = [0]*len(adj_matrix[0])
	
	# Computation of the block sizes (block_dimensions) on comparision with the entries in the look up table
	j = 0
	for i in nodes:
		block_dimensions[j] = block_dim[i]
		j = j+1
		
	
	# Run simulated annealing algorithm for obtaining the optimal floorplan
	best_polish_exp, best_area, best_coord, best_size = annealing(adj_matrix, block_names, block_dimensions)
	
	print("best_coord", best_coord)
	print("block_dimensions", block_dimensions)

	print("Best Polish Expression ", best_polish_exp)
	print("Best Size " + str( best_area) +  " = "+ str( best_size[0]) +  "x" +str( best_size[1]))
	wn = Screen()
	sarah = Turtle()
	wn.setworldcoordinates(0, 0, best_size[0]*3,best_size[1]*3)
	#wn.setworldcoordinates(0, 0, (best_size[0])*1.5+8,(best_size[1])*1.5+8)
	sarah.speed(0)
	placed_coord = best_coord[:]
	loop = 1
	new_best_coord = best_coord[:]
	for i in range(len(best_polish_exp)):
		if(best_polish_exp[i] <= ((len(best_polish_exp) + 1)/2)):
			if (best_coord[best_polish_exp[i]-1][0] == 0 and best_coord[best_polish_exp[i]-1][1] == 0):
				shape(str(best_polish_exp[i]),(best_coord[best_polish_exp[i]-1][0])*2+5,(best_coord[best_polish_exp[i]-1][1])*2,block_dimensions[best_polish_exp[i]-1][0],block_dimensions[best_polish_exp[i]-1][1],sarah)
				#new_best_coord[best_polish_exp[i]-1][0] = best_coord[best_polish_exp[i]-1][0]
				placed_coord[best_polish_exp[i]-1][0] = best_coord[best_polish_exp[i]-1][0]*2+5
				placed_coord[best_polish_exp[i]-1][1] = best_coord[best_polish_exp[i]-1][1]*2
			else:
				shape(str(best_polish_exp[i]),(best_coord[best_polish_exp[i]-1][0])*2+5,(best_coord[best_polish_exp[i]-1][1])*2,block_dimensions[best_polish_exp[i]-1][0],block_dimensions[best_polish_exp[i]-1][1],sarah)
				placed_coord[best_polish_exp[i]-1][0] = best_coord[best_polish_exp[i]-1][0]*2+5
				placed_coord[best_polish_exp[i]-1][1] = best_coord[best_polish_exp[i]-1][1]*2
				loop = loop + 1
	
	# correc_flag indicates if the sizes were corrected using x*2+1 by making grid size as 0.5*0.5 or not. Grid size is 1*1 when correc_flag = 0
	#A,B,xcorrec,ycorrec,correc_flag = grid(best_size[0]*1.5+8,best_size[1]*1.5+8,sarah)
		
	print placed_coord
	grid(best_size[0]*3,best_size[1]*3,sarah)

	wn.exitonclick()
main()