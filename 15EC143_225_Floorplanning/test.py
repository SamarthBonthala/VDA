import random 
def move2(polish_exp):

	polish_exp_temp = polish_exp
	len_exp = len(polish_exp_temp)
	chain = []

	i = 0
	while(i<len(polish_exp_temp)):
		temp = []
		while(polish_exp_temp[i] == 'H' or polish_exp_temp[i] == 'V'):
			temp.append(polish_exp_temp[i])
			i = i+1
		if(len(temp)> 0):
			chain.append(temp)
		i = i+1
	print chain

def move3(polish_exp):
	polish_exp_temp = polish_exp
	len_exp = len(polish_exp_temp)
	polish_exp_original = polish_exp
	operator = ['H','V']
	operand = range(1,len_exp+1)
	adjacent = []
	location = []

	for i in range(len_exp-1):
		temp_arr = []
		if(polish_exp_temp[i] in operator and polish_exp_temp[i+1] in operand):
			temp_arr.append(polish_exp_temp[i])
			temp_arr.append(polish_exp_temp[i+1])
			adjacent.append(temp_arr)
			location.append(i)
		elif(polish_exp_temp[i] in operand and polish_exp_temp[i+1] in operator):
			temp_arr.append(polish_exp_temp[i])
			temp_arr.append(polish_exp_temp[i+1])
			adjacent.append(temp_arr)
			location.append(i)

	len_adj = len(adjacent)
	rand_no = random.randint(0,len(adjacent)-1)

	swap = adjacent[rand_no]
	swap_loc = location[rand_no]

	temp = polish_exp_temp[swap_loc]
	polish_exp_temp[swap_loc] = polish_exp_temp[swap_loc + 1]
	polish_exp_temp[swap_loc + 1] = temp

	return polish_exp_temp,swap_loc

def balloting_prop(polish_exp):

	operator = ['H','V']
	alp_count = 0
	num_count = 0
	i = 0
	flag = 0
	while(i < len(polish_exp)):
		if i in operator:
			alp_count = alp_count + 1
		else:
			num_count = num_count + 1

		if (alp_count < num_count):
			i = i+1
		else:
			flag = 1
			return

	if (flag == 1):
		return 0
	return 1

polish_exp_temp = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H']
print polish_exp_temp
y = balloting_prop(polish_exp_temp)
print y
# polish_exp_temp1, swap_loc = move3(polish_exp_temp)
# while(balloting_prop(polish_exp_temp1, swap_loc) == 0):
# 	polish_exp_temp2, swap_loc = move3(polish_exp_temp)
# 	print polish_exp_temp2
# 	print swap_loc

# #polish_exp_temp = polish_exp_temp1

# print (polish_exp_temp2)

move2(polish_exp_temp)