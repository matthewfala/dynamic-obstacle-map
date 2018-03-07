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
    def __init__(self, view_dist, camera_vector, euler_angle, robot_vector):
        cam = np.linalg.norm(camera_vector)  # NOT WORKING, norm calcs MAGNITUDE
        pos = np.array([1, 0, 0])
        self.dist = view_dist
        #self.angle =
        #self.position =

    def dist_weight(self, dist):
        return dist * pow((RANGE_MAX/dist), EXP_WEIGHT)

# Euler vector rotation
# Ref pg 13 https://www.cs.utexas.edu/~theshark/courses/cs354/lectures/cs354-14.pdf
def euler_vector_rotate(v, alpha, beta, gamma):
    # Rotate about alpha
    x = v.item(0)
    y = v.item(1)
    z = v.item(2)
    v_alpha = np.array([x, y * math.cos(alpha) - z * math.sin(alpha), y * math.sin(alpha) + z * math.cos(alpha)])

    # Rotate about beta
    x = v_alpha.item(0)
    y = v_alpha.item(1)
    z = v_alpha.item(2)
    v_beta = np.array([x * math.cos(beta) + z * math.sin(beta), y, -x * math.sin(beta) + y * math.cos(beta)])

    # Rotate about gamma
    x = v_beta.item(0)
    y = v_beta.item(1)
    z = v_beta.item(2)
    v_gamma = np.array([x * math.cos(gamma) - y * math.sin(gamma), x * math.sin(gamma) + y * math.cos(gamma), z])

    #return fully rotated array
    return v_gamma

# camera direction is in relation to the world
def update_actors(camera_direction, position, actor_list, shadow_list, detected_list):

    # Find all objects in shadow_list that should be updated
    in_view = [] # contains shadow object, and angle range

    angle_ranges = []

    # Upload objects within range
    for s in shadow_list:
        robot_to_object = np.subtract(s.position, position)

        if in_camera_view(camera_direction, robot_to_object):

            # Check if object is within within view range
            dist = np.linalg.norm(robot_to_object)
            if RANGE_MIN < dist < RANGE_MAX:

                # Angle range for dismissing objects behind objects
                dir_vec = robot_to_object
                delta_theta = math.atan(s.radius/dist)

                # Add to in_view array
                in_view.append(s)
                angle_ranges.append([dir_vec, delta_theta])


    # Dismiss shadow objects behind other shadow objects
    # Check for angle overlaps ( Permute ) - Tested
    dismiss_list = []
    for v1i in range(0, len(in_view)-1):
        for v2i in range(v1i + 1, len(in_view)):

            v1 = angle_ranges[v1i][0]
            v2 = angle_ranges[v2i][0]

            theta_v1 = angle_ranges[v1i][1]
            theta_v2 = angle_ranges[v2i][1]

            # get magnitudes
            d_v1 = np.linalg.norm(v1)
            d_v2 = np.linalg.norm(v2)

            # get angle
            angle_between = math.acos(np.dot(v1, v2)/(d_v1 * d_v2))

            # Remove if angle is less than sum of angles (angles overlap)
            if angle_between < theta_v1 + theta_v2:
                print "objects: " + str(v1) + " and " + str(v2) + " overlap"

                # Find which obj is in front
                # v1 is further from robot than v2
                if d_v1 > d_v2:
                    dismiss_list.append(in_view[v1i])
                else:
                    dismiss_list.append(in_view[v2i])

    # remove dismiss list from view
    print "Removing from view: "
    for r in dismiss_list:
        print "Id: " + str(id(r)) + ", Object type: " + str(r.actor_type) + ", Position: " + str(r.position)
        in_view.remove(r)

   # for d in detected_list:
        # Add if within min-view dist
   #     d_radius = VIEW_ERR * d.view_dist + MIN_VIEW_DIST_BUF


    #    if d.dist <


   # for a in in_view:



def in_camera_view(camra_dir, object_dir):
    return True



class ShadowObj:

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
    radius = 0

    mirrored = False

    def __init__ (self, actor_type, position, distance):

        self.actor_type = actor_type

        # give weight to find
        weight = self.dist_weight(distance)
        self.sum_weight += weight
        self.sum_found += weight

        # update position
        self.update_position(position, weight)

        # update radius
        self.update_radius(self.get_radius(distance), weight)

        # min_view_dist and radius
        self.min_view_distance = distance

        #self.sum_r += self.get_radius(self.min_view_distance) * weight

        # increment probed
        self.probed += 1

        print "Id: " + str(id(self)) + ", Object type: " + str(self.actor_type) + ", Position: " + str(self.position) # + ", Distance Viewed: " + self.distance

    # If the object is known to be viewed, probe
    #def probe(self, detected_pos, view_distance):

    def update_position(self, position, weight):
        # give initial position
        self.sum_x += position.item(0) * weight
        self.sum_y += position.item(1) * weight
        self.sum_z += position.item(2) * weight

        # compute new position array
        self.position = np.array([self.sum_x/self.sum_weight, self.sum_y/self.sum_weight, self.sum_z/self.sum_weight])

    def update_radius(self, radius, weight):
        # increment radius
        self.sum_r += radius * weight
        self.radius = self.sum_r / self.sum_weight


    def dist_weight(self, dist):
        return dist * pow((RANGE_MAX/dist), EXP_WEIGHT)

    #def sighted(self, position):

    def get_radius(self, dist):
        return VIEW_ERR * dist


# Create world list
world_list = []

print "########## CREATING OBJECTS #####################"
world_list.append(ShadowObj("buoy", np.array([5, 1, 0]), 10))
world_list.append(ShadowObj("buoy", np.array([4, 0, 0]), 10))
world_list.append(ShadowObj("buoy", np.array([2, 2, 0]), 6))
world_list.append(ShadowObj("buoy", np.array([10, 2, 3]), 10))


update_actors(np.array([2, 1, 0]), np.array([2.7, 0, 0]), world_list, world_list, [])



