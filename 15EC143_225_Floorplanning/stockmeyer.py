# Stockmeyer Algorithm 

# Input: Normalized Polish expression as a list and sizes of each type of block
# Output: List of blocks with the optimal dimensions and the co-ordinate of the lower left corner of each block


def Stockmeyer(polish_exp, block_size):
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
	i = 0 # Loop variable parsing through Polish expression element by element
	j = 0 # Number of times blocks have been combined
	# Computing the area occupied by the orientation of all blocks for the above Polish expression
	while(i < len(polish_exp_temp)):
	
		if (polish_exp_temp[i] in operands):
			stack.append(block_sizes[(polish_exp_temp[i]-1)]) # Appending block sizes to the array
			stk_blk.append(polish_exp_temp[i])
			if (len(stkblk) == 3 and j == 0):
				temp = stkblk[1]
				co_ord[temp-1] = [0,0]
			if (len(stack) == 2 and j == 0):
				temp = stk_blk[0]
				co_ord[temp-1] = [0,0]
				
		if (polish_exp_temp[i] in operators and polish_exp_temp[i] == 'H'):
			right = stack.pop()
			left = stack.pop()
			arr = horizontal_simple(left,right)
			stack.append(arr)
			
			j = j+1
			
			
		if (polish_exp_temp[i] in operators and polish_exp_temp[i] == 'V'):
			top = stack.pop()
			bottom = stack.pop()
			arr = vertical_simple(top,bottom)
			stack.append(arr)
			
			j = j+1
		i = i+1
		
	size = stack.pop()
	area = size[0]*size[1] # Area spanned by this configuration
	
	return area,co_ord

def vertical_simple(L,R):
	L_new = L[:]
	R_new = R[:]
	dim = []
	dim.append(L_new[0]+R_new[0]) # Add the widths as the two blocks are seperated by vertical cut
	dim.append(max(L_new[1],R_new[1])) # Consider the maximum height possible 
	
	return dim

def horizontal_simple(L,R):
	L_new = L[:]
	R_new = R[:]
	dim = []
	dim.append(max(L_new[0],R_new[0])) # Consider the maximum width possible
	dim.append(L_new[1]+R_new[1]) # Add the heights as the two blocks are seperated by vertical cut
	
	return dim
	
def main():

	L = [2,3]
	R = [2,4]
	arr =[]
	Stockmeyer(2,3)
	

main()

def vertical(L,R): # L and R are lists containing the possible dimensions of the two blocks under consideration 
	# Sort the double dimensional array in increasing order of widths
	L_new = L
	L.sort()
	R_new = R
	R.sort()
	print L_new
	print R_new
	combinations = []
	comb_no = []
	len_L = len(L_new[0])
	len_R = len(R_new[0])

	# Optimization to avoid the points not lieing on pareto optimal curve
	for i in range(len_L):
		for j in range(len_R):

			temp_arr = []
			temp_arr1 = [i,j]
			reqd_width = L_new[i][0] + R_new[j][0]
			temp_arr.append(reqd_width)
			if(L_new[i][1] > R_new[j][1]):
				reqd_height = L_new[i][1]
				temp_arr.append(reqd_height)
				combinations.append(temp_arr)
				j = j+1
				#i = i+1
			else:
				reqd_height = R_new[j][1]
				temp_arr.append(reqd_height)
				combinations.append(temp_arr)
				#j = j+1
				i = i+1
			comb_no.append(temp_arr1)
