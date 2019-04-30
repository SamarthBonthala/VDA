import random
import math
import os
import time
import copy
from turtle import *
from Netlist_to_AdjMatrix import netlist_to_adj_mat
# from stockmeyer import area_coord
# from stockmeyer import vertical
# from stockmeyer import horizontal
import numpy as np
from SA_Floorplanning import *
from final_routing import *

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

def main():
    
    print ("Enter the name of the file containing the required netlist")
    filename = input("\n")

    # Converting the netlist to adjacency matrix
    nodes = netlist_to_adj_mat(filename)

    # Take input from the text file containing the adjacency matrix of unpartitioned graph
    adj_matrix = input_func("inp_adj_mat.txt")

    # Look up table for storing the block dimensions in the form of a dictionary
    block_dim = dict()
    block_dim.update({'DFF': [7,6]})
    block_dim.update({'NOT': [1,2]})
    block_dim.update({'AND': [3,4]})
    block_dim.update({'NAND': [2,4]}) 
    block_dim.update({'NOR': [2,4]})
    block_dim.update({'OR': [3,6]})

    block_names = range(1,len(nodes)+1) # Blocks labelled as 1,2,3,4,....,(total_no)
    block_dimensions = [0]*len(adj_matrix[0])

    # Computation of the block sizes (block_dimensions) on comparision with the entries in the look up table
    j = 0
    for i in nodes:
        block_dimensions[j] = block_dim[i]
        j = j+1

    # Run simulated annealing algorithm for obtaining the optimal floorplan
    best_polish_exp, best_area, best_coord, best_size = annealing(adj_matrix, block_names, block_dimensions)

    wn = Screen()
    sarah = Turtle()

    wn.setworldcoordinates(0, 0, best_size[0]*3,best_size[1]*3)
    #wn.setworldcoordinates(0, 0, (best_size[0])*1.5+8,(best_size[1])*1.5+8)
    sarah.speed(0)
    sarah.hideturtle()

    placed_coord = best_coord[:]
    #loop = 1
    new_best_coord = best_coord[:]
    for i in range(len(best_polish_exp)):
        if type(best_polish_exp[i]) is not str:
        	if (best_polish_exp[i]) <= ((len(best_polish_exp) + 1)/2):
        		if (best_coord[best_polish_exp[i]-1][0] == 0 and best_coord[best_polish_exp[i]-1][1] == 0):
        			shape(str(best_polish_exp[i]),(best_coord[best_polish_exp[i]-1][0])*2+5,(best_coord[best_polish_exp[i]-1][1])*2+5,block_dimensions[best_polish_exp[i]-1][0],block_dimensions[best_polish_exp[i]-1][1],sarah)
        			#new_best_coord[best_polish_exp[i]-1][0] = best_coord[best_polish_exp[i]-1][0]
        			placed_coord[best_polish_exp[i]-1][0] = best_coord[best_polish_exp[i]-1][0]*2+5
        			placed_coord[best_polish_exp[i]-1][1] = best_coord[best_polish_exp[i]-1][1]*2+5
        		else:
        			shape(str(best_polish_exp[i]),(best_coord[best_polish_exp[i]-1][0])*2+5,(best_coord[best_polish_exp[i]-1][1])*2+5,block_dimensions[best_polish_exp[i]-1][0],block_dimensions[best_polish_exp[i]-1][1],sarah)
        			placed_coord[best_polish_exp[i]-1][0] = best_coord[best_polish_exp[i]-1][0]*2+5
        			placed_coord[best_polish_exp[i]-1][1] = best_coord[best_polish_exp[i]-1][1]*2+5
        			#loop = loop + 1

    screen_size = best_size[:]
    screen_size[0] = screen_size[0]*6 # *2 for 0.5 resolution, *3 for screen size increase
    screen_size[1] = screen_size[1]*6

    X = list(np.linspace(0, screen_size[0]/2.0, screen_size[0] + 1))
    Y = list(np.linspace(0, screen_size[1]/2.0, screen_size[1] * 2 + 1))

    print (X)
    print (Y)


    obstacle_layer1 = np.zeros((screen_size[1], screen_size[0]), dtype=int)
    obstacle_layer2 = np.zeros((screen_size[1], screen_size[0]), dtype=int)

    # Make the blocks as obstacles
    for i in range(len(block_dimensions)):
    # Extract the size of the block and the left bottom co-ordinates of the block
        xsize = block_dimensions[i][0]
        ysize = block_dimensions[i][1]
        xcoord = placed_coord[i][0]
        ycoord = placed_coord[i][1]

        temp_x = list(np.linspace(xcoord, xcoord + xsize, xsize * 2 + 1))
        temp_y = list(np.linspace(ycoord, ycoord + ysize, ysize * 2 + 1))
        # print("X Coordinates of Block ", i + 1, ": ", temp_x)
        # print("Y Coordinates of Block ", i + 1, ": ", temp_y)
        for j in temp_x:
            # print "X_index for", i, " " , X.index(j)
            for k in temp_y:
                xcoord = screen_size[1] - Y.index(k)
                ycoord = X.index(j)
                obstacle_layer1[xcoord, ycoord] = 1
                obstacle_layer2[xcoord, ycoord] = 1

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
    pin_coord = []

    # Finding pin coordinates
    for i in range(len(placed_coord[0:len(block_dimensions)])):
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

    # Print the obstacle array into a file
    os.system("touch obstacle_layer1.txt")
    f = open("obstacle_layer1.txt", 'w')
    for i in range(obstacle_layer1.shape[0]):
        for j in (range(obstacle_layer1.shape[1])):
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
            temp.append(pin_coord[3 * targets])
            temp.append(pin_coord[3 * targets + 1])
        actual_targets.append(temp)

    print("Pins: ", pin_coord)

    #grid(screen_size[0], screen_size[1], sarah)

    maze_routing(actual_sources, actual_targets, X, Y, obstacle_layer1, obstacle_layer2, screen_size, sarah)

    wn.exitonclick()

main()                                                                                                                                                                                                                                                                                                                                      