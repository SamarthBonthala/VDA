import math

nodes_per_part = math.ceil(7/3)
print nodes_per_part
temp_arr = []
partitions = []
	
loop = 0
for i in range(7):
	if (loop <= nodes_per_part):
		loop = loop + 1
		temp_arr.append(i)
	if (loop > nodes_per_part):
		partitions.append(temp_arr)
		temp_arr = []
		loop = 0
		
if (7%3 != 0):
		print nodes_per_part
		left_over_index = int(nodes_per_part)*len(partitions)
		
		temp_arr = list(range(left_over_index,left_over_index+7%3+1))
		partitions.append(temp_arr)
	
print partitions
