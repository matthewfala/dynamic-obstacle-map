import numpy as np
import math

class World:
    'World class for the physics engine. It is essential a robot class since the robot is the center of the world, which means that everything will move relatively to the robot.'

    # class variables
    gravity = 9.8

    # constructor
    def __init__(self):
        self.actorList = [] # list of actors/objects in the world
        self.velocity = [0, 0, 0] # velocity of the world

        self.w = 0 #math.pi/4 # angular velocity
        self.a = 0 # alpha; angular acceleration
        self.t = 1 # time

    # Continuously update the position of actors in our world.
    def update(self):
        for a in self.actorList:
            a.update(self.w, self.a, self.t)
        
    # Create an object in our world every time we detect one.
    def create_actor(self, actorType, position):
        # Use actorType to determine which type of actor to create.
        if actorType == 0:
            self.actorList.append(Actor(position))
        elif actorType == 1:
            self.actorList.append(Gate(position))
        elif actorType == 2:
            self.actorList.append(Buoy(position))
        elif actorType == 3:
            self.actorList.append(ChipDispenser(position))
        elif actorType == 4:
            self.actorList.append(SlotMachine(position))
        elif actorType == 5:
            self.actorList.append(Roulette(position))
        elif actorType == 6:
            self.actorList.append(Register(position))
        elif actorType == 7:
            self.actorList.append(Bin(position))
        else:
            print "Invalid actor type code."


    # Control movement of the robot/world.
    def move(self, movement):
        for a in self.actorList:
            a.position -= movement

        return 0

    # Display all the actors in our world.
    def display_actors(self):
        for a in self.actorList:
            print '-', a.name, a.position

class Actor:
    'Base class for all actors in our world.'
    name = "Obstacle"
   
    def __init__(self, position):
        self.position = position # position of the actor relative to the robot

    def update(self, v, w, a, t):
        theta = w * t + 0.5 * math.pow(a, t) 
        m = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        self.position = m.dot(self.position)
        
        # translation (provide vehicle velocity)
        dx = np.multiply(v, t)
        self.position = np.subtract(self.position, dx)

class Gate(Actor):
    'Gate class for challenge 1.'
    name = "Gate"

class Buoy(Actor):
    'Buoy class for challenge 2.'
    name = "Buoy"

class ChipDispenser(Actor):
    'ChipDispenser class.'
    name = "Chip Dispenser"

class SlotMachine(Actor):
    'Slot machine class for challenge 3.'
    name = "Slot Machine"

class Roulette(Actor):
    'Roulette class for challenge 3.'
    name = "Roulette"

class Register(Actor):
    'Cashier register class for the final challenge.'
    name = "Register"

class Bin(Actor):
    'Bins/funnels with different colors.'
    name = "Bin"


r = World()
r.create_actor(0, np.array([0,1]))
r.create_actor(1, np.array([0,4]))
print "System: Detected two objects"
r.display_actors()
print ""

while(True):
    print "System: Which way should we move?"
    x = input("x axis: ")
    y = input("y axis: ")
    r.move([x, y])
    r.update()
    r.display_actors()
    print ""
