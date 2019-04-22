from turtle import *

t=turtle.Turtle()
t.speed(0)

wn = Screen()
class Star(turtle.Turtle):
    def __init__(self, x=0, y=0):
        turtle.Turtle.__init__(self)
        self.shape("")
        self.color("")
#Creates the star shape    
    def shape(self, x=0, y=0):
        self.fillcolor("red")
        for i in range(9):
        	self.begin_fill()
        	self.left(90)
        	self.forward(90)
        	self.right(130)
        	self.forward(90)
        self.end_fill()
#I was hoping this would fill the inside        
    def octagon(self, x=0.0, y=0.0):
        turtle.Turtle.__init__(self)

    def octa(self): 
        self.fillcolor("green")
        self.begin_fill()
        self.left(25)
        for x in range(9):
            self.forward(77)
            self.right(40)

#doesn't run with out this
a=Star()
wn.exitonclick()
