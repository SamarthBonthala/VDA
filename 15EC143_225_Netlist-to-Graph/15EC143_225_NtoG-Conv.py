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

	for i in range(len(data)):
		line = data[i].split(" ")
		if (line[0] == "#"):
			no_of_nodes = no_of_nodes + int(line[1])
			check[i] = 1
		if (line[0] == "\n"):
			check[i] = 1			 		
			
	adj_mat = np.zeros((no_of_nodes,no_of_nodes)) # Initialize matrix of size no_of_nodes*no_of_nodes
	
	#print (check)
	# Labelling the nodes as numbers from 0 to (no_of_nodes - 1)
	
	node_names = np.arange(0, no_of_nodes)
	
	# Removal of lines from the txt file to facilitate easy parsing
	f1 = open("s27_new.bench",'a+')
	
	for i in range(len(data)):
		line = data[i].split(" ")
		print line[0]
		print line
		string = data[i]
		f1.write(string)
			
	new_data = f1.readlines()
	print (new_data)
netlist_to_adj_mat()
