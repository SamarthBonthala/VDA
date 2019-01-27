# Netlist to Adjacency Matrix conversion

# Input is a netlist of a benchmark circuit
# Output is an adjacency matrix

import numpy as np
# Input filenames of the form <name>.bench
def netlist_to_adj_mat():
	
	print "Enter the name of the file where the netlist is stored."
	filename = raw_input("\n")
	
	f = open(filename,'r')

	data = f.readlines();
	
	f.close()
	
	# Calculation of number of nodes
	no_of_nodes = 0
	check = np.zeros(len(data))
	inputs = []
	outputs = []
	conn = dict() # Dictionary to store all the entries
	
	for i in range(len(data)):
		line = data[i].split(" ")
		if (line[0] == "#"):
			no_of_nodes = no_of_nodes + int(line[1])
			check[i] = 1
		elif ((data[i].split("("))[0] == "INPUT"):
			temp = (data[i].split("("))[1].split(")")[0]
			inputs.append(temp)
		elif ((data[i].split("("))[0] == "OUTPUT"):
			temp = (data[i].split("("))[1].split(")")[0]
			outputs.append(temp)			 		
		else:
			
		
			
	adj_mat = np.zeros((no_of_nodes,no_of_nodes)) # Initialize matrix of size no_of_nodes*no_of_nodes

	# Labelling the nodes as numbers from 0 to (no_of_nodes - 1)
	
	node_names = np.arange(0, no_of_nodes)
	
	
netlist_to_adj_mat()
