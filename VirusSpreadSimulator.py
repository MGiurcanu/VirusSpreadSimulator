from turtle import *
from random import *
from math import *
from time import *

screen = Screen()
screen.setup(1000, 1000)
w = screen.window_width()
h = screen.window_height()

#---- 1st penturtle
pen1 = Turtle()
pen1.color("black")
pen1.hideturtle()
pen1.up()
pen1.goto(-250, 200)
pen1.down()

#---- 2nd penturtle
pen2 = Turtle()
pen2.color("black")
pen2.hideturtle()
pen2.up()
pen2.goto(-250, 185)
pen2.down()

#---- 3rd penturtle
pen3 = Turtle()
pen3.color("black")
pen3.hideturtle()
pen3.up()
pen3.goto(-250, 170)
pen3.down()

#---- 4th penturtle
pen4 = Turtle()
pen4.color("black")
pen4.hideturtle()
pen4.up()
pen4.goto(-250, 155)
pen4.down()

#---- constants
MAX_MOVE_LEN = 40
DEATH_PCT = 10
STARTING_INFECTION_PCT = 20  # how many people are infected at the start of the simulation?
INFECTION_DISTANCE = 40      # how close does a person have to be to get infected?
INFECTION_PCT = 80           # if you are close to a sick person, how likely are you to get infected?
CONTAGIOUS_TIME = 5          # after a certain number of days of being ill, you are no longer contagious
DAYS = 100

#--------start of class
class Person(Turtle):
    # a person is a turtle with an x,y location
    # a healthy, non-immune person is blue
    # a dead person is gray
    # an infected person is red
    # an immune (alive) is green
    def __init__(self):
        super().__init__()
        # a person is a turtle in a random postion
        self.penup()
        self.shape("circle")

        self.speed(0)
        self.setpos(randint(-w/2, w/2), randint(-h/2, h/2))
        self.setheading(randint(0,360))
        self.shape('turtle')
        self.neighbors = []
        self.overallHealth = randint(0, 100)
        self.alive = True
        self.immune = False
        if randint(0,100) < STARTING_INFECTION_PCT:
            self.ill = True
            self.contagiousTime = CONTAGIOUS_TIME
            self.color('red')
        else:
            self.ill = False
            self.contagiousTime = 0
            self.color('blue')



    def move(self):
        if self.alive:
            self.setheading(randint(0,360))
            self.forward(randint(0,MAX_MOVE_LEN))
    
    
    def moveControlledFAKE(self):
        if self.alive:
            self.forward(randint(0,40))
            
    def moveControlled(self):
        if self.alive:
            self.forward(randint(0,60))


    def dist(self, other):
        x1 = self.xcor()
        y1 = self.ycor()
        x2 = other.xcor()
        y2 = other.ycor()
        d = sqrt((x1-x2)**2  +  (y1-y2)**2)
        return d

    def infect(self, other):  # assume other is within infection distance
        if other.ill and not self.immune:
            if randint(0,100) < INFECTION_PCT:
                self.ill = True
                self.contagiousTime = CONTAGIOUS_TIME
                self.color('red')

    def checkInfection(self):
        for p in self.neighbors:
            self.infect(p)

    def endContagious(self):
        if self.ill:
            self.contagiousTime = self.contagiousTime - 1
            if self.contagiousTime <= 0:
                if randint(0,100) < DEATH_PCT:
                    self.alive = False
                    self.ill = False
                    self.immune = True
                    self.color('gray')
                else:
                    self.ill = False
                    self.immune = True
                    self.color('green')


    def findNeighbors(self, peopleList):
        self.neighbors = []
        for p in peopleList:
            if p != self and p.alive and self.dist(p) < INFECTION_DISTANCE:
                self.neighbors.append(p)
    

#-------end of class

# --- function definitions
peopleList = []
def makePeople(numPeople):
    for i in range(numPeople):
        p = Person()
        peopleList.append(p)


def moveAll():
    for p in peopleList:
        if p.xcor() > w/2:
            p.setheading(randint(135, 225))
            p.moveControlled()
        elif p.xcor() < (-w/2):
            p.setheading(randint(-45, 45))
            p.moveControlled()
        elif p.ycor() > h/2:
            p.setheading(randint(225, 315))
            p.moveControlled()
        elif p.ycor() < (-h/2):
            p.setheading(randint(45, 135))
            p.moveControlled()
        
        else:
            p.move()
            

    
def findAllNeighbors():
    for p in peopleList:
        p.findNeighbors(peopleList)

def infectAll():
    for p in peopleList:
        p.checkInfection()

def endContagiousAll():
    for p in peopleList:
        p.endContagious()

def oneDay():
    findAllNeighbors()
    endContagiousAll()
    infectAll()
    moveAll()

def pctIll():
    totalPop = len(peopleList)
    numIll = 0
    for p in peopleList:
        if p.ill:
            numIll += 1
    pct = numIll/totalPop * 100
    return pct

def pctDead():
    totalPop = len(peopleList)
    numDead = 0
    for p in peopleList:
        if not p.alive:
            numDead += 1
    pct = numDead/totalPop * 100
    return pct

def pctImmune():
    totalPop = len(peopleList)
    numImmune = 0
    for p in peopleList:
        if p.alive and p.immune:
            numImmune += 1
    pct = numImmune/totalPop * 100
    return pct

def pctNotImmune():
    totalPop = len(peopleList)
    numNotImmune = 0
    for p in peopleList:
        if p.alive and not p.immune:
            numNotImmune += 1
    pct = numNotImmune/totalPop * 100
    return pct

def inputs():
    pen1.write(": " + str(), False, 'left', font = ('Cooper Black', 13, 'bold'))
    pen2.write(": " + str(), False, 'left', font = ('Cooper Black', 13, 'bold'))
    pen3.write(": " + str(), False, 'left', font = ('Cooper Black', 13, 'bold'))
    pen4.write(": " + str(), False, 'left', font = ('Cooper Black', 13, 'bold'))
def results():
    
    pen1.up()
    pen1.goto(-250, 130)
    pen1.down()
    pen1.write("Ill: " + str(pctIll()), False, 'left', font = ('Cooper Black', 13, 'bold'))
    
    pen2.up()
    pen2.goto(-250, 115)
    pen2.down()
    pen2.write("Dead: " + str(pctDead()), False, 'left', font = ('Cooper Black', 13, 'bold'))
    
    pen3.up()
    pen3.goto(-250, 100)
    pen3.down()
    pen3.write("Alive and immune: " + str(pctImmune()), False, 'left', font = ('Cooper Black', 13, 'bold'))
    
    pen4.up()
    pen4.goto(-250, 85)
    pen4.down()
    pen4.write("Alive and not immune: " + str(pctNotImmune()), False, 'left', font = ('Cooper Black', 13, 'bold'))

#-----main program
screen.tracer(0,0)
makePeople(100)
screen.update()
sleep(1)
for i in range(DAYS):
    oneDay()
    sleep(0.001)
    screen.update()    



print ( "Ill:", pctIll()   )
print ( "Dead:", pctDead()   )
print ( "Alive and immune:", pctImmune()   )
print ( "Alive and not immune:", pctNotImmune()   )

inputs()
results()


