# Kernighan Lin Algorithm for Circuit Partitioning
#Authors: Samarth Bonthala, Tarun Mittal
f = open("adj_matrix.txt",'r')

data = f.readlines()
adj_matrix = []

for i in data:
	temp = i.split()
	temp = [int(j) for j in temp]
	adj_matrix.append(temp)
  
print (adj_matrix)

no_of_nodes = len(adj_matrix[0])

# Adding a dummy node
if (len(adj_matrix[0])%2 != 0):
	no_of_nodes = no_of_nodes + 1
	for i in range(no_of_nodes-1):
		adj_matrix[i].append(0)
	temp = [0]*(no_of_nodes)
	adj_matrix.append(temp)
			
# Random partitioning
	 
locked = [0]*len(adj_matrix[0]) # To indicate if node is in locked state or not
A = []
B = []

for i in range(len(locked)):
	if(i<(len(locked)/2)):
		A.append(i)
  	else:
  		B.append(i)

print(A)
print(B)

# Computation of D

D = [0]*no_of_nodes
for i in range(no_of_nodes):
	
	if i in A:
	
		for j in range(no_of_nodes):
	
			if j in A:
				D[i] = D[i] - adj_matrix[i][j]
			else:
				D[i] = D[i] + adj_matrix[i][j]
	else:
		for j in range(no_of_nodes):
	
			if j in B:
				D[i] = D[i] - adj_matrix[i][j]
			else:
				D[i] = D[i] + adj_matrix[i][j]
		
print(D)

# Calculation of g
		
max_g = 100 
while( max_g > 0 ):

	g = [[0 for i in range(no_of_nodes)] for j in range(no_of_nodes)]
	max_g = 0
	max_i = -1
	max_j = -1
	for i in A:
		if (locked[i] ==0):
			for j in B:
				if(locked[j] == 0):
				
					g[i][j] = D[i]+D[j]-2*adj_matrix[i][j]
					if(g[i][j] > max_g):
						max_g = g[i][j]
						max_i = i
						max_j = j

	print (g)
	print(max_g)
	print(max_i)
	print(max_j)

	if(max_g>0):
		locked[max_i] = 1
		locked[max_j] = 1
		A.remove(max_i)
		B.remove(max_j)
		A.append(max_j)
		B.append(max_i)
	
	for i in range(no_of_nodes):
		
		if(locked[i] == 0):
			
			if i in A:
				x = 1
			else:
				x = -1
				
			D[i] = D[i] + 2*x* ( adj_matrix[i][max_i] - adj_matrix[i][max_j])
			
	print(D)
	  

print(A)
print(B)

