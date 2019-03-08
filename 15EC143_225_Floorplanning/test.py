import random 
def move2(polish_exp):

	polish_exp_temp = polish_exp
	len_exp = len(polish_exp_temp)
		
	# To create operator and operand array seperately from the Polish expression
	operator = ['H','V']
	operand = range(1,len_exp+1)
	chains = []
	location = []
	i = 0
	temp_arr = []
	while(i<len_exp-1):
		
		if(polish_exp_temp[i] in operator):
			temp_arr.append(polish_exp_temp[i])
			location.append(i)
		j = i+1

		while(j<len_exp):
			if(polish_exp_temp[j] in operator):
				temp_arr.append(polish_exp_temp[j])
			elif(polish_exp_temp[j] in operand):
				chains.append(temp_arr)
				location.append(i)
				temp_arr = []
				i = j+1
			j = j+1
		i = i+1

	print chains
	print location

def move3(polish_exp):
	polish_exp_temp = polish_exp
	len_exp = len(polish_exp_temp)

	operator = ['H','V']
	operand = range(1,len_exp+1)
	adjacent = []
	location = []

	for i in range(len_exp-1):
		temp_arr = []
		if((polish_exp_temp[i] in operator and polish_exp_temp[i+1] in operand) or (polish_exp_temp[i] in operand and polish_exp_temp[i+1] in operator)):
			temp_arr.append(polish_exp_temp[i])
			temp_arr.append(polish_exp_temp[i+1])
			adjacent.append(temp_arr)
			location.append(i)
	len_adj = len(adjacent)
	rand_no = random.randint(0,len(adjacent))

	swap = adjacent[rand_no]
	swap_loc = location[rand_no]

	temp = polish_exp_temp[swap_loc]
	polish_exp_temp[swap_loc] = polish_exp_temp[swap_loc + 1]
	polish_exp_temp[swap_loc + 1] = temp

	print polish_exp_temp

polish_exp_temp = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H']
print polish_exp_temp
move3(polish_exp_temp)

