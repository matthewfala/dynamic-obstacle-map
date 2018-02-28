import numpy as np
import math

class World:
    'World class for the physics engine.'

    def __init__(self):
        self.actorList = [] # container for the objects in this world
        
        # define position of objects
        actorList.append(Robot(np.array([0, 0, 0])))
        actorList.append(Gate(np.array([5, 3, 0])))
        actorList.append(Buoy(np.array([7, 5, 0])))
        actorList.append(ChipDispenser(np.array([7, 7, 0])))
        actorList.append(SlotMachine(np.array([14, 5, 0])))
        actorList.append(ChipDispenser(np.array([14, 7, 0])))
        actorList.append(Roulette(np.array([20, 10, 0])))
        actorList.append(Register(np.array([24, 13, 0])))
        actorList.append(Bin(np.array([24, 14, 0])))

    # Create new objects in case we encounter unaccounted things.
    # There could be multiple buoys and bins.
    def create_actor(self, actorType, position):
        if actorType == 0:
            self.actorList.append(Actor(position))
        elif actorType == 1:
            self.actorList.append(Buoy(position))
        elif actorType == 2:
            self.actorList.append(Bin(position))
        else:
            print "Invalid actor type."

    # Display everything we know about the world.
    def display_actors(self):
        for a in self.actorList:
            print '-', a.name, a.position

class Actor:
    'Base class for all actors.'
    name = "Obstacle"

    def __init__(self, position):
        self.position = position # position of actor in the world

class Robot(Actor):
    'Robot class for our robot.'
    name = "Robot"

    def __init__(self, position):
        self.velocity = [0, 0, 0] # initial velocity
        self.w = 0 # angular velocity
        self.a = 0 # alpha; angular acceleration
        self.t = 0 # time

class Buoy(Actor):
    'Buoy class.'
    name = "Buoy"

class ChipDispenser(Actor):
    'Chip dispenser class. Could have at least 2.'
    name = "Chip Dispenser"

class SlotMachine(Actor):
    'Slot machine class.'
    name = "Slot Machine"

class Roulette(Actor):
    'Roulette class.'
    name = "Roulette"

class Register(Actor):
    'Cashier Register class.'
    name = "Register"

class Bin(Actor):
    'Bins/funnels with different colors.'
    name = "Bin"

r = World()
