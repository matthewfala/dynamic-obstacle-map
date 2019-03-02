###############################
#       Simulation World      #
#       By Matthew Fala       #
###############################

# Description: Simulation world intakes a set of virtual obstacles such as buoys and goal posts along
# with their location. As a fake robot probes these obstacles, distance is calculated to the obstacle
# and a gaussian randomized error proportional to distance is output is output for the obstacle
# fake_error_per_dist: this variable sets the gaussian error value.

# Usage: The DOM (Dynamic Obstacle Map) System's goal is to undo gaussian error and determine some
# average position based on multiple queries. The simulation_world provides a realistic gaussian
# error model, close to what will be outputted from the CV system.

import numpy as np
import random

# Settings
fake_error_per_dist = .05

# Create world lists
world_list = []


# Virtual World Object Configurations
print "########## CREATING OBJECTS #####################"
# world_list.append(ShadowObj("buoy", np.array([5, 1, 0]), 10))
# world_list.append(ShadowObj("buoy", np.array([4, 0, 0]), 10))
# world_list.append(ShadowObj("buoy", np.array([2, 2, 0]), 6))
# world_list.append(ShadowObj("buoy", np.array([10, 2, 3]), 10))


# update_actors(np.array([2, 1, 0]), np.array([2.7, 0, 0]), world_list, world_list, [])

fake_coords = []

# fake_coords.append(["buoy", np.array([5, 2, 3])])
# fake_coords.append(["buoy", np.array([10, 0, 0])])
# fake_coords.append(["buoy", np.array([.1, .1, .2])])
# fake_coords.append(["buoy", np.array([1, 2, 2])])
# fake_coords.append(["buoy", np.array([6, 3, 1])])
# fake_coords.append(["buoy", np.array([2, 5, 0])])
# fake_coords.append(["buoy", np.array([2, 3, 1])])
fake_coords.append(["buoy", np.array([0, 0, 0])])


# A fake query of the CV ROS topic
def get_detected_list(robot_pos, f_coords):
    detected_list = []
    for f in f_coords:
        dist = np.linalg.norm(robot_pos-f[1])
        err = fake_error_per_dist * dist
        x = random.gauss(f[1].item(0), err)
        y = random.gauss(f[1].item(1), err)
        z = random.gauss(f[1].item(2), err)

        #print "Random x y z generated: " + str(x) + ", " + str(y) + ", " + str(z)

        fake_pos = np.array([x, y, z])

        detected_list.append(DetectedObject(f[0], fake_pos))
    return detected_list


# CV Obstacle (Replace with ROS MSG)
class DetectedObject:

    def __init__(self, _actor_type, _position):
        self.actor_type = _actor_type
        self.position = _position
        self.radius = 1

    def get_actor_type(self):
        return self.actor_type

    def get_position(self):
        return self.position

    def get_radius(self):
        return self.radius


# Simplified map (of actors)
class DumbWorld:

    def __init__(self, my_actor_list):
        self.actor_list = my_actor_list

    def create_actor(self, actorType, position):
        new_actor = DumbActor(actorType, position)
        self.actor_list.append(new_actor)
        return new_actor


# Simplified actor
class DumbActor:

    def __init__(self, actor_type, position):
        self.actor_type = actor_type
        self.position = position

    def get_position(self):
        return self.position

    def update_position(self, new_position):
        self.position = new_position

