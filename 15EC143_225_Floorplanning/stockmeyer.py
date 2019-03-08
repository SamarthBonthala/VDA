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

	sarah.goto((x+a/2.0),(y+b/2.0))
	sarah.write(label, False, align="center")

def check_if_done(polish_exp_temp, inorder, done, done_index):
	for i in range(len(done)):
		if (polish_exp_temp[i] in inorder):
			done_index = i + 1
		else:
			break

	return done_index

def post_to_inorder(polish_exp_temp,operators,operands):
	inorder = []
	num_stack = []
	char_stack = []
	num = 1
	done = [0]*len(polish_exp_temp)
	done_index = 0

	i = 0
	while(len(inorder)<len(polish_exp_temp)):

		x = polish_exp_temp[i]

		if( (x in operands) and (num == 1) ):
			#print("1")
			inorder.append(x)
			num = 0
			i = check_if_done(polish_exp_temp,inorder,done,done_index)
			#num_stack.clear()
			#char_stack.clear()
			del num_stack[:]
			del char_stack[:]
		elif((x in operands) and (num == 0) ):
			#print("2")
			num_stack.append(x)
			i = i + 1

		elif((x in operators) and ((len(num_stack) - 1) == (len(char_stack)))):
			#print("3")
			inorder.append(x)
			num = 1
			i = check_if_done(polish_exp_temp,inorder,done,done_index)
			# num_stack.clear()
			# char_stack.clear()
			if(len(num_stack)>0):
				inorder.append(num_stack[0])
				num = 0
				i = check_if_done(polish_exp_temp,inorder,done,done_index)

			del num_stack[:]
			del char_stack[:]

		elif((x in operators) and ((len(num_stack) - 1) != (len(char_stack)))):
			#print("4")
			char_stack.append(x)
			i = i + 1


		#print("inorder", inorder)
	return inorder
def area_coord(polish_exp_temp, block_size):
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

		i = i+1
	
	# co_ord[no_of_blocks-1] = new[:]	
	size = stack.pop()
	area = size[1][0]*size[1][1] # Area spanned by this configuration


	inorder = post_to_inorder(polish_exp_temp, operators, operands)
	print(inorder)


	new = [0,0]
	co_ord[inorder[0]-1] = new[:]
	i = 1
	num = 0
	op = 'V'

	while(i<len(inorder)):
		if(inorder[i] == 'V'):
			co_ord[inorder[i + 1]-1] = [co_ord[inorder[i-1]-1][0] + block_sizes[inorder[i-1]-1][0], co_ord[inorder[i-1]-1][1] ]
			#co_ord[inorder[i + 1]-1] = [new[0] + ] 
		elif(inorder[i] == 'H'):
			co_ord[inorder[i + 1]-1] = [co_ord[inorder[i-1]-1][0], block_sizes[inorder[i-1]-1][1]+ co_ord[inorder[i-1]-1][1] ]


		print("co_ord", co_ord)
		i = i + 2


	return area,co_ord,size

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
	area, node_coord,size = area_coord(2,3)	

	wn = Screen()
	sarah = Turtle()
	wn.setworldcoordinates(0, 0, size[1][0]+5,size[1][1]+5)
	sarah.speed(0)

	node_type = [0,1,2,3,4]

	block_dimensions = [[9,6],[6,8],[3,6],[3,7],[6,5]]

	block_sizes = [[2,4],[1,3],[3,3],[3,5],[3,2],[5,3],[1,2],[2,4]]

	print("coord",node_coord)
	for i in range(len(block_sizes)):
		shape(str(i+1),node_coord[i][0],node_coord[i][1],block_sizes[i][0],block_sizes[i][1],sarah)

	wn.exitonclick()

main()

