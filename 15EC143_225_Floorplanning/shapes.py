
from turtle import *

def square(x,y,sarah):
    sarah.goto(x,y)
    sarah.pendown()
    for i in [0,1,2,3]:      #repeat four times
        sarah.forward(50)
        sarah.left(90)
    sarah.penup()

def shape(x,y,a,b,sarah):
	sarah.goto(x,y)
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

wn = Screen()
sarah = Turtle()
sarah.speed(0)
square(0,0,sarah)
square(0,100,sarah)
shape(100,0,5,7,sarah)
wn.exitonclick()