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
#from SA_Floorplanning import *
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

# Assuming we get the the area of the circuit from other functions/subroutines of SA_Floorplanning.py file

# We have block_dimensions array too
#best_polish_exp, best_area, best_coord, best_size = annealing(adj_matrix, block_names, block_dimensions)
best_coord = [[8, 0], [0, 9], [0, 1], [10, 12], [0, 0], [8, 5], [0, 6], [12, 5], [10, 9], [12, 12], [0, 15], [8, 9], [12, 9], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
best_polish_exp = [5, 3, 'H', 7, 'H', 1, 6, 8, 'V', 'H', 'V', 2, 12, 9, 4, 'H', 13, 10, 'H', 'V', 'V', 'V', 11, 'H', 'H']
best_size = [16,18]
best_area = 288
block_dimensions = [[8, 5], [8, 5], [8, 5], [2, 1], [2, 1], [4, 3], [4, 3], [4, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3]]
# new_best_size has the new block dimensions - after placement
screen_size = best_size[:]
screen_size[0] = screen_size[0]*6 # *2 for 0.5 resolution, *3 for screen size increase 
screen_size[1] = screen_size[1]*6

# A,B will have the grid points on the x-axis and y-axis
# A,B = grid(new_best_size[0],new_best_size[1],sarah)

X = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0]
Y = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0]
print len(X)
print len(Y)
# Grid size by default will be 1*1
# We can draw a wire in between the grid at 0.5 point 

# obstacle - 2D list stores a 1 in that location if a block is present else stores 0
obstacle = np.zeros((screen_size[0], screen_size[1]))
pins = np.zeros((screen_size[0] + 1, screen_size[1] + 1), dtype=str)

# x axis locations are defined by entries of A and y axis locations are defined by entries of B
placed_coord = [[21, 0], [5, 18], [5, 2], [25, 24], [5, 0], [21, 10], [5, 12], [29, 10], [25, 18], [29, 24], [5, 30], [21, 18], [29, 18], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
pin_coord = []
# Finding pin coordinates
for i in range(len(placed_coord[0:13])):
	temp = [0, 0]
	temp[0] = placed_coord[i][0]
	temp[1] = placed_coord[i][1] + block_dimensions[i][1]/2.0
	pin_coord.append(temp)
	temp = [0, 0]
	temp[0] = placed_coord[i][0] + block_dimensions[i][0]
	temp[1] = placed_coord[i][1] + block_dimensions[i][1]/2.0
	pin_coord.append(temp)

print pin_coord

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

# Make the blocks as obstacles
for i in range(len(block_dimensions)):
	# Extract the size of the block and the left bottom co-ordinates of the block
	xsize = block_dimensions[i][0]
	ysize = block_dimensions[i][1]
	xcoord = placed_coord[i][0]
	ycoord = placed_coord[i][1]

	temp_x = list(np.linspace(xcoord,xcoord+xsize,xsize*2+1))
	temp_y = list(np.linspace(ycoord,ycoord+ysize,ysize*2+1))
	for j in temp_x:
		#print "X_index for", i, " " , X.index(j)
		for k in temp_y:
			#print "Y_index for ", i, " ", Y.index(k)
			obstacle[Y.index(k), X.index(j)] = 1


for i in range(len(pin_coord)):
	pins[Y.index(pin_coord[i][1]), X.index(pin_coord[i][0])] = 'p'

os.system("touch pins.txt")
f = open("pins.txt", 'w')
for i in range(pins.shape[0]):
	for j in reversed(range(pins.shape[1])):
		f.write(str(pins[i, j]))
		f.write("  ")
	f.write("\n")	
	
f.close()

# Print the obstacle array into a file
os.system("touch obstacle.txt")
f = open("obstacle.txt", 'w')
for i in range(obstacle.shape[0]):
	for j in reversed(range(obstacle.shape[1])):
		f.write(str(obstacle[i, j]))
		f.write("  ")
	f.write("\n")	
	
f.close()



# wn.exitonclick()

