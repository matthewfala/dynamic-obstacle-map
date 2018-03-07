import numpy as np
import math

# Constants

# Position and hits are weighted by an exponent of 1 / view distance
EXP_WEIGHT = 5

# Error (meters) / Dist
VIEW_ERR = .5 / 7

MIN_VIEW_DIST_BUF = 1

# Stop sensing things that are too close or too far
RANGE_MIN = 1
RANGE_MAX = 20

# View ACTIVATE_VIEWS times before activating obj
ACTIVATE_VIEWS = 100

# Probabilities
CREATE_PROBABILITY = .5
REMOVE_PROBABILITY = .2
DESTROY_RECORD_PROBABILITY = .05



# Create Shadow World
shadow_list = []

class DetectedObj:
    def __init__(self, view_dist, camera_vector):
        cam = np.linalg.norm(camera_vector)
        pos = np.array([1, 0, 0])
        self.dist = view_dist
        self.angle =
        self.position =

    def dist_weight(self, dist):
        return dist * pow((RANGE_MAX/dist), EXP_WEIGHT)


def update_actors(actor_list, shadow_list, detected_list):

    # Find all objects in shadow_list that should be updated
    in_view = []

    for s in shadow_list:





    for d in detected_list:
        # Add if within min-view dist

        d_radius = VIEW_ERR * d.view_dist + MIN_VIEW_DIST_BUF


        if d.dist <


    for a in in_view:







class shadow_obj:

    # number of times obj should be in view
    probed = 0

    # weighted finds
    sum_weight = 0 # weight is only added to if object should be seen
    sum_found = 0

    # weighted sums
    sum_x = 0
    sum_y = 0
    sum_z = 0

    # numpy position array
    position = np.array([0,0,0])

    # weighted radius sums by hit
    sum_r = 0

    mirrored = False

    def __init__ (self, actor_type, position, distance):
        self.actor_type = actor_type

        # give weight to find
        weight = self.dist_weight(distance)
        self.sum_weight += weight
        self.sum_found += weight



        # min_view_dist and radius
        self.min_view_distance = distance
        self.sum_r += self.get_radius(self.min_view_distance) * weight

        # increment probed
        self.probed += 1

    # If the object is known to be viewed, probe
    def probe(self, detected_pos, view_distance):

    def update_position(self, position, weight):
        # give initial position
        self.sum_x += position.item(0) * weight
        self.sum_y += position.item(1) * weight
        self.sum_z += position.item(2) * weight

        # compute new position array
        self.position = np.array([self.sum_x/self.sum_weight, self.sum_y/self.sum_weight, self.sum_z/self.sum_weight])

    def dist_weight(self, dist):
        return dist * pow((RANGE_MAX/dist), EXP_WEIGHT)

    def sighted(self, position):

    def get_radius(self, dist):
        return VIEW_ERR * dist


