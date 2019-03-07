# Stockmeyer Algorithm 

# Input: Normalized Polish expression as a list and sizes of each type of block
# Output: List of blocks with the optimal dimensions and the co-ordinate of the lower left corner of each block
from turtle import *

def shape(label,x,y,a,b,sarah):
	sarah.goto(x,y)
	sarah.pendown()
	sarah.forward(a)
	sarah.left(90)
	sarah.forward(b)
	sarah.left(90)
	sarah.forward(a)
	sarah.left(90)
	sarah.forward(b)
	sarah.left(90)
	sarah.penup()

	sarah.goto((x+a/2),(y+b/2))
	sarah.write(label, False, align="center")


def area_coord(polish_exp, block_size):
	# Construct a tree from the polish expression
	polish_exp_temp = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H']
	#polish_exp_temp = [1,2,'V',3,'V',4,'V',5,'V',6,'V',7,'V',8,'V']
	
	operands = []
	operators = ['H','V']
	block_sizes = [[2,4],[1,3],[3,3],[3,5],[3,2],[5,3],[1,2],[2,4]]
	for i in polish_exp_temp:
		if i in operators:
			continue
		else:
			operands.append(i)
		
	no_of_blocks = len(operands)
	co_ord = [0]*no_of_blocks
	
	# Parsing through the Polish expression is same as Post order traversal of a binary tree
	# Stack creation to find the minimum area of the block
	# Convention: xyH means x is below y and xyV means x is to the left of y
	
	stack = []
	stk_blk = []
	new = [0,0]
	i = 0 # Loop variable parsing through Polish expression element by element
	j = 0 # Number of times blocks have been combined
	# Computing the area occupied by the orientation of all blocks for the above Polish expression
	while(i < len(polish_exp_temp)):
	
		if (polish_exp_temp[i] in operands):
			#stack.append(block_sizes[(polish_exp_temp[i]-1)]) # Appending block sizes to the array
			stack.append([polish_exp_temp[i],block_sizes[(polish_exp_temp[i]-1)]])
			print(polish_exp_temp[i])
			print("stack",stack)
			# stk_blk.append(polish_exp_temp[i])
			# if (len(stk_blk) == 3 and j == 0):
			# 	temp = stk_blk[1]
			# 	co_ord[temp-1] = [0,0]
			# if (len(stack) == 2 and j == 0):
			# 	temp = stk_blk[0]
			# 	co_ord[temp-1] = [0,0]
				
		elif (polish_exp_temp[i] in operators and polish_exp_temp[i] == 'V'):
			right = stack.pop()
			print("right",right)
			left = stack.pop()
			print("left",left)
			arr = vertical(left[1],right[1])
			if(right[0]>no_of_blocks):
				x =  right[2]
			else:
				x = right[0]
			stack.append([left[0]*no_of_blocks,arr,x])
			print("stack H",stack)

			if(left[0]>no_of_blocks and right[0]>no_of_blocks):
				continue
			elif(right[0]<no_of_blocks and left[0] > no_of_blocks):
				co_ord[right[0]-1] = [co_ord[left[2]-1][0] + block_sizes[left[2]-1][0],co_ord[left[2]-1][1]]
			elif(right[0]>no_of_blocks and left[0] < no_of_blocks):
				co_ord[left[0]-1] = [co_ord[right[2]-1][0] + block_sizes[right[2]-1][0],co_ord[right[2]-1][1]]
			elif(right[0]<no_of_blocks and left[0] < no_of_blocks):
				co_ord[left[0]-1] =  new[:]
				co_ord[right[0]-1] = [new[0]+ left[1][0] , new[1] ]
			
			new[:] = arr[:]

			print("new", new)
			print("coord",co_ord)

			#j = j+1
			
			
		elif (polish_exp_temp[i] in operators and polish_exp_temp[i] == 'H'):
			top = stack.pop()
			print("top",top)
			if(len(stack)==0):
				stack.append(top)
				break
			bottom = stack.pop()
			print("bottom",bottom)
			arr = horizontal(top[1],bottom[1])
			if(top[0]>no_of_blocks):
				x =  top[2]
			else:
				x = top[0]
			stack.append([bottom[0]*no_of_blocks,arr,x])
			print("stack V",stack)
			if(top[0]>no_of_blocks and bottom[0]>no_of_blocks):
				continue
			elif(top[0]<no_of_blocks and bottom[0]>no_of_blocks):
				co_ord[top[0]-1] = [co_ord[bottom[2]-1][0], co_ord[bottom[2]-1][1] + block_sizes[bottom[2]-1][1]]
			elif(top[0]>no_of_blocks and bottom[0]<no_of_blocks):
				co_ord[bottom[0]-1] = [co_ord[top[2]-1][0], co_ord[top[2]-1][1] + block_sizes[top[2]-1][1]]
			elif(top[0]<no_of_blocks and bottom[0]<no_of_blocks):
				co_ord[bottom[0]-1] = new[:]
				co_ord[top[0]-1] = [new[0] + bottom[1][0] , new[1]]
			new[:] = arr[:]

			print("new", new)
			print("coord",co_ord)
			#j = j+1
		i = i+1
	
	co_ord[no_of_blocks-1] = new[:]	
	size = stack.pop()
	area = size[0]*size[1] # Area spanned by this configuration
	

	return area,co_ord

def vertical(L,R):
	L_new = L[:]
	R_new = R[:]
	dim = []
	dim.append(L_new[0]+R_new[0]) # Add the widths as the two blocks are seperated by vertical cut
	dim.append(max(L_new[1],R_new[1])) # Consider the maximum height possible 
	
	return dim

def horizontal(L,R):
	L_new = L[:]
	R_new = R[:]
	dim = []
	dim.append(max(L_new[0],R_new[0])) # Consider the maximum width possible
	dim.append(L_new[1]+R_new[1]) # Add the heights as the two blocks are seperated by vertical cut
	print("dim", dim)

	return dim
	
def main():

	# L = [2,3]
	# R = [2,4]
	# arr =[]
	# Stockmeyer(2,3)
	area, node_coord = area_coord(2,3)	

	wn = Screen()
	sarah = Turtle()
	wn.setworldcoordinates(0, 0, 50, 50)
	sarah.speed(0)

	node_type = [0,1,2,3,4]

	block_dimensions = [[9,6],[6,8],[3,6],[3,7],[6,5]]

	block_sizes = [[2,4],[1,3],[3,3],[3,5],[3,2],[5,3],[1,2],[2,4]]

	print("coord",node_coord)
	for i in range(len(block_sizes)):
		shape(str(i+1),node_coord[i][0],node_coord[i][1],block_sizes[i][0],block_sizes[i][1],sarah)

	wn.exitonclick()

main()

