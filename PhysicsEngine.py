import numpy as np
import math
class World:
    'World class for the physics engine. It is essential a robot class since the robot is the center of the world, which means that everything will move relatively to the robot.'

    # class variables
    gravity = 9.8

    # constructor
    def __init__(self):
        self.actorList = [] # list of actors
        self.velocity = [0, 0, 0] # velocity of the world
        #self.facing = [1, 0, 0] # initially facing x axis
        self.a = 0
        self.w = math.pi/4
        self.t = 1
    # main functions
    def update(self): # keep updating the postiion of all objects
        for a in self.actorList:
            a.update(self.w,self.a,self.t)
    
        
    def create_object(self, name, position):
        self.actorList.append(Actor(name, position))
    def move(self, direction, acceleration):
        # update velocity and position
        return 0

    # helper functions
    def display_objects(self):
        print self.actorList



class Actor():
    'Base class for all objects in the world.'
   
    def __init__(self, name, position):
        self.name = name
        self.position = position
    def update(self,w,a,t):
        theta = w * t + .5 * math.pow(a,t) 
        m = np.array([[math.cos(theta), -math.sin(theta)],[math.sin(theta), math.cos(theta)]])
        self.position = m.dot(self.position)
class Gate:
    'Gate class for challenge 1.'

    def __init__(self, name, position):
        self.name = name
        self.position = position

class Buoy:
    'Buoy class for challenge 2.'

    def __init__(self, name, position):
        self.name = name
        self.position = position

class ChipDispenser:
    'ChipDispenser class for challenge 3.'

    def __init__(self, name, position):
        self.name = name
        self.position = position

class Slot:
    'Slot machine class for challenge 4.'

    def __init__(self, name, position):
        self.name = name
        self.position = position

class Roulette:
    'Roulette class for challenge 5.'

    def __init__(self, name, position):
        self.name = name
        self.position = position
r = World()
r.create_object("one",np.array([0,1]))
r.update()
r.actorList[0].position