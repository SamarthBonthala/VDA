from turtle import *
import numpy as np

def shape(label,x,y,a,b,sarah):
	sarah.goto(x,y)
	sarah.pendown()
	sarah.forward(a)
	sarah.left(90)
	sarah.forward(b)
	sarah.left(90)
	sarah.forward(a)
	sarah.left(90)
	sarah.forward(b)
	sarah.left(90)
	sarah.penup()

	sarah.goto((x+a/2),(y+b/2))
	sarah.write(label, False, align="center")

def grid(x,y,sarah):
	A = list(np.linspace(0,x,x+1))
	B = list(np.linspace(0,y,y+1))
	print A
	print B

	for i in A:

		sarah.goto(i,0)
		sarah.pencolor("red")
		sarah.pendown()
		sarah.left(90)
		sarah.forward(y)
		sarah.penup()
		sarah.right(90)

	for j in B:

		sarah.goto(0,j)
		sarah.pencolor("blue")
		sarah.pendown()
		sarah.forward(x)
		sarah.penup()

wn = Screen()
sarah = Turtle()
best_size = [26, 10]
wn.setworldcoordinates(0, 0, best_size[0]*2, best_size[1]*2)
sarah.speed(0)
# Best Size is 26*10
best_coord = [[0, 0], [0, 6], [0, 11], [8, 0], [0, 5], [0, 22], [2, 19], [4, 22], [2, 25], [2, 16], [0, 16], [0, 19], [0, 25], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

block_dimensions = [[8, 5], [8, 5], [8, 5], [2, 1], [2, 1], [4, 3], [4, 3], [4, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3]]

best_polish_exp = [1, 2, 'V', 4, 3, 6, 'V', 'V', 'H', 5, 7, 'H', 11, 'H', 9, 'H', 'V', 12, 8, 10, 'H', 'V', 13, 'H', 'V']

# for i in range(len(best_polish_exp)):
# 		if(best_polish_exp[i] < ((len(best_polish_exp) + 1)/2)):
# 			shape(str(best_polish_exp[i]),(best_coord[best_polish_exp[i]-1][0])+1,(best_coord[best_polish_exp[i]-1][1])+1,block_dimensions[best_polish_exp[i]-1][0],block_dimensions[best_polish_exp[i]-1][1],sarah)

grid(best_size[0]*2, best_size[1]*2,sarah)

wn.exitonclick()

