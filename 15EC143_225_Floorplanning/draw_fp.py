from turtle import *

def shape(label,x,y,a,b,sarah):
	sarah.goto(x*10,y*10)
	sarah.pendown()
	sarah.forward(a*10)
	sarah.left(90)
	sarah.forward(b*10)
	sarah.left(90)
	sarah.forward(a*10)
	sarah.left(90)
	sarah.forward(b*10)
	sarah.left(90)
	sarah.penup()

	sarah.goto((x+a/2)*10,(y+b/2)*10)
	sarah.write(label, False, align="center")


wn = Screen()
sarah = Turtle()
sarah.speed(0)

node_type = [0,1,2,3,4]

block_dimensions = [[9,6],[6,8],[3,6],[3,7],[6,5]]

node_coord = [[0,0],[9,0],[0,6],[3,6],[6,8]]


for i in range(len(node_type)):
	shape(str(i),node_coord[i][0],node_coord[i][1],block_dimensions[node_type[i]][0],block_dimensions[node_type[i]][1],sarah)

wn.exitonclick()