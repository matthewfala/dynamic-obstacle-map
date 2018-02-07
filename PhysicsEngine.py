class World:
    'World class for the physics engine.'
    # class variables
    gravity = 9.8

    # constructor
    def __init__(self):
        self.actorList = {}
        self.numOfObjects = 0

    def display_objects(self):
        print self.actorList

    def create_object(self, name, weight, position, velocity):
        self.actorList[self.numOfObjects] = Actor(name, weight, position, velocity)
        numOfObjects += 1

class Actor:
    'Base class for all objects in the world.'
    
    def __init__(self, name, weight,  position, velocity):
        self.name = name
        self.weight = weight
        self.position = position
        self.velocity = velocity

    def get_details():
        print self.name, self.weight, self.position, self.velocity

def update():
    return

# initialization
x = World()
x.create_object
