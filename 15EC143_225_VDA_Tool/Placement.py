import random
import math
import os
import time
import copy
from turtle import *
from Netlist_to_AdjMatrix import netlist_to_adj_mat
from stockmeyer import area_coord
from stockmeyer import vertical
from stockmeyer import horizontal
import numpy as np
#from SA_Floorplanning import *
def input_func(filename):

	f = open(filename,'r')

	data = f.readlines()
	adj_matrix = []

	for i in data:
		temp = i.split()
		temp = [int(j) for j in temp]
		adj_matrix.append(temp)
  	
  	return adj_matrix
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

def grid(x,y,sarah):
	A = list(np.linspace(0,x,x*2+1))
	B = list(np.linspace(0,y,y*2+1))

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

	return A,B 
def draw(layer1, layer2):

	# Use turtle graphics here for drawing the routes
	return

def cleanup(routing_grid, X, Y):
	for i in X:
		for j in Y:
			routing_grid[(i, j)] = [0, 0, 0]

	return routing_grid

def compute_least_cost(routing_grid,  points, coordinates, new_predecessor, current_predecessor):
	cost = 1
	bendcost = 3
	viacost = 10

	if new_predecessor != current_predecessor:
		cost += bendcost
	if cost < routing_grid[tuple(coordinates)][0]:
		routing_grid[tuple(coordinates)][0] = cost + routing_grid[points][0]
		routing_grid[tuple(coordinates)][1] = new_predecessor

	return routing_grid



def maze_routing(actual_sources, actual_targets, X, Y, obstacle_layer1, obstacle_layer2, layer1, layer2, screen_size):

	# Via Cost = 10, Bend Cost = 3
	routing_grid = dict()
	# Key part of routing_grid dictionary is the lower left edge coordinates of the grid cell 
	# Value part of the routing_grid dictionary is a list consisting of [least_cost, predecessor, reached] 
	routing_grid = cleanup(routing_grid, X, Y)

	for i in range(len(actual_sources)):
		if (len(actual_targets[i]) > 1):
			multi_point_net(routing_grid, actual_sources[i], actual_targets[i], X, Y, obstacle_layer1, obstacle_layer2, layer1, layer2, screen_size)
		else:
			single_point_net(routing_grid, actual_sources[i], actual_targets[i][0], X, Y, obstacle_layer1, obstacle_layer2, layer1, layer2, screen_size)


def single_point_net(routing_grid, source, target, X, Y, obstacle_layer1, obstacle_layer2, layer1, layer2, screen_size):

	# Mazerouting involves three fundamental steps
	# 1. Expansion
	# 2. Backtrace to obtain least cost path
	# 3. Clean-up the grid cells and block the grids used up by the least cost route obtained
	# Predecessor convention - N = -1; S = -2; E = -3; W = -4; U = -5; D = -6

	routing_grid = cleanup(routing_grid, X, Y)

	wavefront = dict()
	wavefront[tuple(source)] = [0, 0, 1]
	wavefront_copy = copy.deepcopy(wavefront)
	# Key part of wavefront dictionary is the lower left edge coordinates of the grid cell
	# Value part of the wavefront dictionary is a list consisting of [least_cost, predecessor, layer]
	while(routing_grid[tuple(target)][2] != 1):
		for points in wavefront.keys():
			coordinates = []
			if points == source:
				if points[0]+0.5 < screen_size[0]:
					coordinates = [points[0] + 0.5, points[1]]
				else:
					print "Unroutable Net: ", source, " ", target
					continue
				routing_grid[tuple(coordinates)] = [1, -4, 1]
				wavefront_copy[tuple(coordinates)] = [1, -4, 1]
			else:	
				if wavefront[points][2] == 1:
					if points[0]+0.5 < screen_size[0]:
						if obstacle_layer1[Y.index(points[1]), X.index(points[0]+0.5)] != 1:
							coordinates = [points[0]+0.5, points[1]]
							# Cost parameters = routing_grid, predecessor of new wavefront point, predecessor of current wavefront point
							routing_grid = compute_least_cost(routing_grid, points, coordinates, -4, wavefront[points][1])
							# routing_grid[coordinates] = [cost, -4, 1]
							wavefront_copy[tuple(coordinates)] = [routing_grid[tuple(coordinates)][0], -4, 1]
					if points[0]-0.5 > 0:
						if obstacle_layer1[Y.index(points[1]), X.index(points[0]-0.5)] != 1:
							coordinates = [points[0]+0.5, points[1]]
							# Cost parameters = routing_grid, predecessor of new wavefront point, predecessor of current wavefront point
							routing_grid = compute_least_cost(routing_grid, points, coordinates, -3, wavefront[points][1])
							# routing_grid[coordinates] = [cost, -3, 1]
							wavefront_copy[tuple(coordinates)] = [routing_grid[tuple(coordinates)][0], -3, 1]
					if points[1] + 0.5 < screen_size[1]:
						if obstacle_layer1[Y.index(points[1] + 0.5), X.index(points[0])] != 1:
							coordinates = [points[0], points[1] + 0.5]
							# Cost parameters = routing_grid, predecessor of new wavefront point, predecessor of current wavefront point
							routing_grid = compute_least_cost(routing_grid, points, coordinates, -2, wavefront[points][1])
							# routing_grid[coordinates] = [cost, -2, 1]
							wavefront_copy[coordinates] = [routing_grid[tuple(coordinates)][0], -2, 1]
					if points[1] - 0.5 > 0:
						if obstacle_layer1[Y.index(points[1] - 0.5), X.index(points[0])] != 1:
							coordinates = [points[0], points[1] - 0.5]
							# Cost parameters = routing_grid, predecessor of new wavefront point, predecessor of current wavefront point
							routing_grid = compute_least_cost(routing_grid, points, coordinates, -1, wavefront[points][1])
							# routing_grid[coordinates] = [cost, -1, 1]
							wavefront_copy[tuple(coordinates)] = [routing_grid[tuple(coordinates)][0], -1, 1]


			wavefront_copy.pop(points)
		print "Old Wavefront: ", wavefront
		print "New Wavefront: ", wavefront_copy
		print "Routing Grid: "
		for i in X:
			for j in Y:
				if routing_grid[(i, j)] != [0, 0, 0]:
					print routing_grid[(i, j)]
		wavefront.clear()		
		wavefront = copy.deepcopy(wavefront_copy)				





# Assuming we get the the area of the circuit from other functions/subroutines of SA_Floorplanning.py file

# We have block_dimensions array too
#best_polish_exp, best_area, best_coord, best_size = annealing(adj_matrix, block_names, block_dimensions)
#best_coord = [[8, 0], [0, 9], [0, 1], [10, 12], [0, 0], [8, 5], [0, 6], [12, 5], [10, 9], [12, 12], [0, 15], [8, 9], [12, 9], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
best_coord = [[7, 0], [0, 8], [0, 0], [0, 6], [7, 6], [3, 14], [0, 14], [12, 14], [8, 18], [8, 14], [10, 14], [15, 0], [6, 14], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
#best_polish_exp = [5, 3, 'H', 7, 'H', 1, 6, 8, 'V', 'H', 'V', 2, 12, 9, 4, 'H', 13, 10, 'H', 'V', 'V', 'V', 11, 'H', 'H']
best_polish_exp = [3, 1, 'V', 4, 2, 'V', 5, 'V', 'H', 7, 6, 13, 'V', 10, 11, 'V', 9, 'H', 8, 'V', 'V', 'V', 'H', 12, 'V']
#best_size = [16,18]
best_size = [17,20]
#best_area = 288
best_area = 374
#block_dimensions = [[8, 5], [8, 5], [8, 5], [2, 1], [2, 1], [4, 3], [4, 3], [4, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3]]
block_dimensions = [[7, 6], [7, 6], [7, 6], [1, 2], [1, 2], [3, 4], [3, 6], [3, 6], [2, 4], [2, 4], [2, 4], [2, 4], [2, 4]]
# x axis locations are defined by entries of A and y axis locations are defined by entries of B
#placed_coord = [[21, 0], [5, 18], [5, 2], [25, 24], [5, 0], [21, 10], [5, 12], [29, 10], [25, 18], [29, 24], [5, 30], [21, 18], [29, 18], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
placed_coord = [[19, 5], [5, 21], [5, 5], [5, 17], [19, 17], [11, 33], [5, 33], [29, 33], [21, 41], [21, 33], [25, 33], [35, 5], [17, 33], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
# new_best_size has the new block dimensions - after placement
screen_size = best_size[:]
screen_size[0] = screen_size[0]*6 # *2 for 0.5 resolution, *3 for screen size increase 
screen_size[1] = screen_size[1]*6
# A,B will have the grid points on the x-axis and y-axis
# A,B = grid(new_best_size[0],new_best_size[1],sarah)

#X = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0]
X = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0]
#Y = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0]
Y = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0] 

# Grid size by default will be 0.5*0.5
# We can draw a wire in between the grid at 0.5 point 

# obstacle - 2D list stores a 1 in that location if a block is present else stores 0
obstacle_layer1 = np.zeros((screen_size[0], screen_size[1]))
obstacle_layer2 = np.zeros((screen_size[0], screen_size[1]))

#routing_grid = np.zeros((screen_size[0], screen_size[1]))
# Multilayered routing - needed to avoid the condition of non-routability
layer1 = np.zeros((screen_size[0], screen_size[1]))
layer2 = np.zeros((screen_size[0], screen_size[1]))

# pins = np.zeros((screen_size[0] + 1, screen_size[1] + 1), dtype=str)

# Make the blocks as obstacles
for i in range(len(block_dimensions)):
	# Extract the size of the block and the left bottom co-ordinates of the block
	xsize = block_dimensions[i][0]
	ysize = block_dimensions[i][1]
	xcoord = placed_coord[i][0]
	ycoord = placed_coord[i][1]

	temp_x = list(np.linspace(xcoord,xcoord+xsize,xsize*2+1))
	temp_y = list(np.linspace(ycoord,ycoord+ysize,ysize*2+1))
	print temp_x
	print temp_y
	for j in temp_x:
		#print "X_index for", i, " " , X.index(j)
		for k in temp_y:
			#print "Y_index for ", i, " ", Y.index(k)
			obstacle_layer1[Y.index(k), X.index(j)] = 1


pin_coord = []
# Finding pin coordinates
for i in range(len(placed_coord[0:13])):
	temp = [0, 0]
	temp[0] = placed_coord[i][0]
	temp[1] = placed_coord[i][1] + block_dimensions[i][1]/4.0
	pin_coord.append(temp)
	temp = [0, 0]
	temp[0] = placed_coord[i][0]
	temp[1] = placed_coord[i][1] + block_dimensions[i][1]*3/4.0
	pin_coord.append(temp)
	temp = [0, 0]
	temp[0] = placed_coord[i][0] + block_dimensions[i][0]
	temp[1] = placed_coord[i][1] + block_dimensions[i][1]/2.0
	pin_coord.append(temp)

# print pin_coord

# wn = Screen()
# sarah = Turtle()
# wn.setworldcoordinates(0, 0, best_size[0]*3,best_size[1]*3)
# #wn.setworldcoordinates(0, 0, (best_size[0])*1.5+8,(best_size[1])*1.5+8)
# sarah.speed(0)

# for i in range(len(best_polish_exp)):
# 	if(best_polish_exp[i] <= ((len(best_polish_exp) + 1)/2)):
# 		if (best_coord[best_polish_exp[i]-1][0] == 0 and best_coord[best_polish_exp[i]-1][1] == 0):
# 			shape(str(best_polish_exp[i]),(best_coord[best_polish_exp[i]-1][0])*2+5,(best_coord[best_polish_exp[i]-1][1])*2,block_dimensions[best_polish_exp[i]-1][0],block_dimensions[best_polish_exp[i]-1][1],sarah)
# 		else:
# 			shape(str(best_polish_exp[i]),(best_coord[best_polish_exp[i]-1][0])*2+5,(best_coord[best_polish_exp[i]-1][1])*2,block_dimensions[best_polish_exp[i]-1][0],block_dimensions[best_polish_exp[i]-1][1],sarah)


# for i in range(len(pin_coord)):
# 	pins[Y.index(pin_coord[i][1]), X.index(pin_coord[i][0])] = 'p'

# os.system("touch pins.txt")
# f = open("pins.txt", 'w')
# for i in range(pins.shape[0]):
# 	for j in reversed(range(pins.shape[1])):
# 		f.write(str(pins[i, j]))
# 		f.write("  ")
# 	f.write("\n")	
	
# f.close()

# Print the obstacle array into a file
os.system("touch obstacle_layer1.txt")
f = open("obstacle_layer1.txt", 'w')
for i in range(obstacle_layer1.shape[0]):
	for j in reversed(range(obstacle_layer1.shape[1])):
		f.write(str(obstacle_layer1[i, j]))
		f.write("  ")
	f.write("\n")	
	
f.close()

adj_matrix = input_func("inp_adj_mat.txt")
adj_matrix = np.array(adj_matrix)
# Assigning source and target pairs
source_target_pairs = []
for i in range(adj_matrix.shape[0]):
	connections = adj_matrix[i, :]
	connections_nonzero = list(np.nonzero(connections)[0])
	if len(connections_nonzero) != 0:
		source_target_pairs.append([i, connections_nonzero])

# Estimation of actual source and target
# Left pin of every block is Input and right pin is Output
actual_sources = []
actual_targets = []
for pair in source_target_pairs:
	# Right pin goes into the actual_sources array
	actual_sources.append(pin_coord[3*pair[0]+2])
	temp = []
	# Left pins go into the actual_targets array
	for targets in pair[1]:
		temp.append(pin_coord[3*targets])
		temp.append(pin_coord[3*targets+1])
	actual_targets.append(temp)

print  "Pins: ", pin_coord
print "Sources: ", actual_sources
print "Targets: ", actual_targets

maze_routing(actual_sources, actual_targets, X, Y, obstacle_layer1, obstacle_layer2, layer1, layer2, screen_size)


# wn.exitonclick()

