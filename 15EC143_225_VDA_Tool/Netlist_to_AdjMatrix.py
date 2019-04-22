# Netlist to Adjacency Matrix conversion

# Input is a netlist of a benchmark circuit
# Output is an adjacency matrix

import os

# Input filenames of the form <name>.bench
def netlist_to_adj_mat(filename):

	f = open(filename,'r')

	data = f.readlines();
	
	f.close()
	
	# Calculation of number of nodes
	inputs = []
	outputs = []
	new_arr = []
	init_outputs =[]
	gates_n_op = []
	gate_names_ops = dict() # Dictionary to store all the entries
	nodes = []
	# Extracting information from file
	for i in range(len(data)):
		line = data[i].split(" ")
		if (line[0] == "#"):
			continue
		elif ((data[i].split("("))[0] == "INPUT"):
			temp = (data[i].split("("))[1].split(")")[0]
			inputs.append(temp)
		elif ((data[i].split("("))[0] == "OUTPUT"):
			temp = (data[i].split("("))[1].split(")")[0]
			outputs.append(temp)			 		
		elif (data[i] != '\n'):
			temp1 = (data[i].split("=")[0]).split(" ")[0]
			init_outputs.append(temp1)
			temp2 = (data[i].split("=")[1])
			temp3 = temp2.strip()
			gates_n_op.append(temp3)
			temp_data = temp3.split("(")[0]
			nodes.append(temp_data)
		else:
			continue
	
	# Creating a dictionary gate_names_ops for the gates_n_op array
	loop = 0
	for info in gates_n_op:
		temp2 = info.split("(")[0]
		temp = (info.split("(")[1]).split(")")[0]
		edges = temp.split(", ")
		gate_names_ops[loop] = edges
		loop = loop + 1

	
	no_of_nodes = len(gate_names_ops)
	adj_mat = [[0 for i in range(no_of_nodes)] for j in range(no_of_nodes)] # Initialize matrix of size no_of_nodes*no_of_nodes
	
	# Once an edge is found out, the adjacency matrix is updated, both adj_mat[i][j] and adj_mat[j][i] with 1 assuming graph is undirected 
	
	for value in init_outputs:
		indx = init_outputs.index(value)
		for node in gate_names_ops:
			if value in gate_names_ops[node]:
				adj_mat[node][indx] = 1
				adj_mat[indx][node] = 1
	
	os.system("touch inp_adj_mat.txt")
	f = open("inp_adj_mat.txt", 'w')
	for i in range(len(adj_mat[0])):
		for j in range(len(adj_mat[0])):
			f.write(str(adj_mat[i][j]))
			f.write(" ")	
		
		f.write("\n")
	f.close()
	return nodes

#if __name__ == '__main__':
#	nodes = netlist_to_adj_mat()
