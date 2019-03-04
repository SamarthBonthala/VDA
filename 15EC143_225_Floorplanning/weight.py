import math

# Input Function
def input_func(filename):

	f = open(filename,'r')

	data = f.readlines()
	adj_matrix = []

	for i in data:
		temp = i.split()
		temp = [int(j) for j in temp]
		adj_matrix.append(temp)
  	
  	return adj_matrix;
  	


adj_matrix = input_func("inp_adj_mat.txt")

n = len(adj_matrix[0])

node_type = [1,2,1,0,0]
block_dimensions = [[2,3],[4,5],[2,4]]

node_coord = [[0,0],[2,0],[0,3],[3,3],[0,7]]

weight = 0

for i in range(n):

	x1 = node_coord[i][0] + (block_dimensions[node_type[i]][0])/2
	y1 = node_coord[i][1] + (block_dimensions[node_type[i]][1])/2

	for j in range(n):
		if(adj_matrix[i][j] !=0):
			x2 = node_coord[j][0] + (block_dimensions[node_type[j]][0])/2
			y2 = node_coord[j][1] + (block_dimensions[node_type[j]][1])/2

			dist = math.sqrt((x2-x1)**2 + (y2 - y1)**2)

			weight = weight + dist*adj_matrix[i][j]

print(weight)