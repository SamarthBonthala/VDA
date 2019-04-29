# Stockmeyer Algorithm 

# Input: Normalized Polish expression as a list and sizes of each type of block
# Output: List of blocks with the optimal dimensions and the co-ordinate of the lower left corner of each block
from turtle import *
# Definition for a  binary tree node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        self.coord = None
        self.dim = None

class Solution:
    # @param inorder, a list of integers
    # @param postorder, a list of integers
    # @return a tree node
    # 12:00
    def buildTree(self, inorder, postorder):
        if not inorder or not postorder:
            return None
        
        root = TreeNode(postorder.pop())
        #print("root", root.val)
        inorderIndex = inorder.index(root.val)
        #print("inorderIndex", inorderIndex)

        root.right = self.buildTree(inorder[inorderIndex+1:], postorder)
        root.left = self.buildTree(inorder[:inorderIndex], postorder)

        return root


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

	# print("aana polish_exp_temp", polish_exp_temp)
	# print("aana operators", operators)
	# print("aana operands", operands)
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
			# print("1")
			inorder.append(x)
			num = 0
			i = check_if_done(polish_exp_temp,inorder,done,done_index)
			# print("i", i)
			#num_stack.clear()
			#char_stack.clear()
			del num_stack[:]
			del char_stack[:]
		elif((x in operands) and (num == 0) ):
			# print("2")
			num_stack.append(x)
			i = i + 1

		elif((x in operators) and ((len(num_stack) - 1) == (len(char_stack)))):
			# print("3")
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
			# print("4")
			char_stack.append(x)
			i = i + 1


		#print("inorder", inorder)
	return inorder

def get_coord(root, block_sizes, combined_size,combined_size_list, polish_exp_temp, co_ord, operands):

	if(root.val in operands):
		co_ord[root.val - 1] = root.coord
		# print("co_ord 11", co_ord)

	if(root.left == None and root.right == None):
		return co_ord

	if(root.val[0] == 'H'):
		# print("HHH")
		# print("root co", root.coord)
		# print("rootleft", root.left.val)
		# print("rootright", root.right.val)
		# print("polish_exp_temp exp chu", polish_exp_temp)
		# print("root left index", polish_exp_temp.index(root.left.val))
		root.left.coord = root.coord
		root.right.coord = [root.coord[0], root.coord[1] + combined_size[polish_exp_temp.index(root.left.val)][1]]

		co_ord = get_coord(root.left, block_sizes, combined_size,combined_size_list, polish_exp_temp, co_ord, operands)
		co_ord = get_coord(root.right, block_sizes, combined_size, combined_size_list, polish_exp_temp, co_ord, operands)

	if(root.val[0] == 'V'):
		# print("VVV")
		# print("root co", root.coord)
		# print("rootleft", root.left.val)
		# print("rootright", root.right.val)
		# print("root left index", polish_exp_temp.index(root.left.val))
		root.left.coord = root.coord
		root.right.coord = [root.coord[0] + combined_size[polish_exp_temp.index(root.left.val)][0], root.coord[1]]

		co_ord = get_coord(root.left, block_sizes, combined_size,combined_size_list, polish_exp_temp, co_ord, operands)
		co_ord = get_coord(root.right, block_sizes, combined_size,combined_size_list, polish_exp_temp, co_ord, operands)	


	return co_ord

def area_coord(polish_exp_temp, block_sizes):
	# Construct a tree from the polish expression
	#polish_exp_temp = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H']
	#polish_exp_temp = [1,2,'V',3,'V',4,'V',5,'V',6,'V',7,'V',8,'V']
	
	# print("aaya aaya", polish_exp_temp)
	operands = []
	operators = ['H','V']
	#block_sizes = [[2,4],[1,3],[3,3],[3,5],[3,2],[5,3],[1,2],[2,4]]
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
	size = []
	new = [0,0]
	combined_size = []
	combined_size_list = []
	vcount = 0
	hcount = 0
	updated_operators = []
	updated_pol_exp = polish_exp_temp[:]
	i = 0 # Loop variable parsing through Polish expression element by element
	j = 0 # Number of times blocks have been combined
	# Computing the area occupied by the orientation of all blocks for the above Polish expression
	#print("ttptptptp")
	#print("polish_exp_temp", polish_exp_temp)
	while(i < len(polish_exp_temp)):
	
		if (polish_exp_temp[i] in operands):
			#stack.append(block_sizes[(polish_exp_temp[i]-1)]) # Appending block sizes to the array
			#print("polish_exp_temp[i]",polish_exp_temp[i])
			#print("block_sizes[(polish_exp_temp[i]-1)]", block_sizes[(polish_exp_temp[i]-1)])
			stack.append(block_sizes[(polish_exp_temp[i]-1)])
			#print(polish_exp_temp[i])
			#print("stack",stack)
				
		elif (polish_exp_temp[i] in operators and polish_exp_temp[i] == 'V'):
			#print(polish_exp_temp)
			#print(stack)
			right = stack.pop()
			#print("right",right)
			left = stack.pop()
			#print("left",left)
			arr = vertical(left,right)
			size = arr[:]
			stack.append(arr[:])
			combined_size_list.append('V' + str(vcount))
			combined_size.append(arr)
			updated_operators.append(('V' + str(vcount)))
			updated_pol_exp[i] = 'V' + str(vcount)
			vcount = vcount + 1
			
			
		elif (polish_exp_temp[i] in operators and polish_exp_temp[i] == 'H'):
			top = stack.pop()
			#print("top",top)
			# if(len(stack)==0):
			# 	stack.append(top)
			# 	break
			bottom = stack.pop()
			#print("bottom",bottom)
			arr = horizontal(top,bottom)
			size = arr[:]
			stack.append(arr[:])
			combined_size_list.append('H' + str(hcount))
			combined_size.append(arr)
			updated_operators.append(('H' + str(hcount)))
			updated_pol_exp[i] = 'H' + str(hcount)
			hcount = hcount + 1
		
		i = i+1
	
	# co_ord[no_of_blocks-1] = new[:]	
	
	#print("stack just been", stack)
	#size = stack.pop()
	#print("size", size)
	# print("block_sizes", block_sizes)
	final_combined_size = [0]*len(polish_exp_temp)

	for i in range(len(polish_exp_temp)):
		if(polish_exp_temp[i] in operands):
			# print("updated_pol_exp[i]	",polish_exp_temp[i])
			final_combined_size[i] = block_sizes[polish_exp_temp[i] - 1]
		else:
			final_combined_size[i] = combined_size[combined_size_list.index(updated_pol_exp[i])]


	# print("combined_size", combined_size)
	# print("final_combined_size", final_combined_size)
	area = size[0]*size[1] # Area spanned by this configuration

	# print("updated_operators", updated_operators)
	# print("polish_exp_temp", polish_exp_temp)
	# print("updated_pol_exp", updated_pol_exp)
	inorder = post_to_inorder(updated_pol_exp, updated_operators, operands)
	

	#print(inorder)

	yet_another_pol = updated_pol_exp[:]

	root = Solution().buildTree( inorder, yet_another_pol)
	root.dim = size[:]
	root.coord = [0,0]
	co_ord = [[0,0]]*len(polish_exp_temp)
	# co_ord.append(root.coord)
	# print("root", root.coord[0])
	# print("polish_exp_temp 121", polish_exp_temp)
	co_ord = get_coord(root, block_sizes, final_combined_size, combined_size_list, updated_pol_exp, co_ord, operands)

	# new = [0,0]
	# co_ord[inorder[0]-1] = new[:]
	# i = 1
	# num = 0
	# op = 'V'

	# while(i<len(inorder)):
	# 	if(inorder[i] == 'V'):
	# 		co_ord[inorder[i + 1]-1] = [co_ord[inorder[i-1]-1][0] + block_sizes[inorder[i-1]-1][0], co_ord[inorder[i-1]-1][1] ]
	# 		#co_ord[inorder[i + 1]-1] = [new[0] + ] 
	# 	elif(inorder[i] == 'H'):
	# 		co_ord[inorder[i + 1]-1] = [co_ord[inorder[i-1]-1][0], block_sizes[inorder[i-1]-1][1]+ co_ord[inorder[i-1]-1][1] ]


	# 	#print("co_ord", co_ord)
	# 	i = i + 2



	return area,co_ord,size

def vertical(L,R):
	L_new = L[:]
	#L_new = copy.deepcopy(L)
	R_new = R[:]
	#R_new = copy.deepcopy(R)
	dim = []
	dim.append(L_new[0]+R_new[0]) # Add the widths as the two blocks are seperated by vertical cut
	dim.append(max(L_new[1],R_new[1])) # Consider the maximum height possible 
	
	return dim

def horizontal(L,R):
	L_new = L[:]
	#L_new = copy.deepcopy(L)
	R_new = R[:]
	#R_new = copy.deepcopy(R)
	dim = []
	dim.append(max(L_new[0],R_new[0])) # Consider the maximum width possible
	dim.append(L_new[1]+R_new[1]) # Add the heights as the two blocks are seperated by vertical cut
	#print("dim", dim)

	return dim
	
# def main():

# # 	# L = [2,3]
# # 	# R = [2,4]
# # 	# arr =[]
# # 	# Stockmeyer(2,3)
# 	area, node_coord,size = area_coord(2,3)	

# 	wn = Screen()
# 	sarah = Turtle()
# 	wn.setworldcoordinates(0, 0, size[0]+5,size[1]+5)
# 	sarah.speed(0)

# 	node_type = [0,1,2,3,4]

# 	block_dimensions = [[9,6],[6,8],[3,6],[3,7],[6,5]]

# 	block_sizes = [[2,4],[1,3],[3,3],[3,5],[3,2],[5,3],[1,2],[2,4]]

# 	print("coord",node_coord)
# 	for i in range(len(block_sizes)):
# 		shape(str(i+1),node_coord[i][0],node_coord[i][1],block_sizes[i][0],block_sizes[i][1],sarah)

# 	wn.exitonclick()

# main()

