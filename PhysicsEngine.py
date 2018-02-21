class World:
    'World class for the physics engine. It is essential a robot class since the robot is the center of the world, which means that everything will move relatively to the robot.'

    # class variables
    gravity = 9.8

    # constructor
    def __init__(self):
        self.actorList = {} # list of actors
        self.velocity = [0, 0, 0] # velocity of the world
        self.facing = [1, 0, 0] # initially facing x axis

    # main functions
    def update(self): # keep updating the postiion of all objects

    def create_object(self, name, position, velocity):
        self.actorList[self.numOfObjects] = Actor(name, position, velocity)

    def move(self, direction, acceleration):
        # update velocity and position


    # helper functions
    def display_objects(self):
        print self.actorList


class Actor:
    'Base class for all objects in the world.'
    
    def __init__(self, name, position):
        self.name = name
        self.position = position

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



# initialization
x = World()
x.create_object
