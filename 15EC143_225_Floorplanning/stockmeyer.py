# Stockmeyer Algorithm 

# Input: Normalized Polish expression as a list and sizes of each type of block
# Output: List of blocks with the optimal dimensions and the co-ordinate of the lower left corner of each block





# Parsing through the Polish expression is same as Post order traversal of a binary tree

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



	print (combinations)
	print (comb_no)


L = [[2,3],[3,2]]
R = [[2,4],[4,2]]

vertical(L,R)