

############################################
#       DOM (Dynamic Obstacle Map)         #
#       By Matthew J.W. Fala               #
############################################

# Description: The DOM (Dynamic Obstacle Map) was written for USC AUV by Matthew J.W. Fala.
# It consolidates all Computer Vision Obstacle discoveries and dynamically generates a probability map.
# Objects that have a high threshold probability of existence are logged to a FOM or Fixed Obstacle Map on
# the client side.

# Python Interface
#
# Call update_actors to update the world

# ROS Interface (Needs Implementation)
#
# Interface: The interface is ROS Message.
# ROS Topic: /fom
#
# Message Parameters:
#   string cmd
#   string type
#   int id
#   float64 x
#   float64 y
#   float64 z


# Imports
import numpy as np
import math
from shadow_object import ShadowObj

import settings as const

# Division Precision (Removed in v1.2)
# PROBABILITY_PRECISION = 10 ** 3
# PRECISION_BITS = PROBABILITY_PRECISION.bit_length()

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
        return dist * pow((const.RANGE_MAX/dist), const.EXP_WEIGHT)


# to connect detected with digital
class Pair:
    def __init__(self, digital, physical):
        self.digital = digital
        self.physical = physical


# not dependant on actor type
# camera direction is in relation to the world
def update_actors(world, camera_direction, robot_position, actor_list, shadow_list, detected_list):

    # Find all objects in shadow_list that should be updated
    in_view = []  # contains shadow object, and angle range
    in_close_proximity = []  # contains objects that are too close to camera to detect // These will block the camera
                             # use for dismissals

    angle_ranges = []

    # list of mirrored shadow objects
    shadow_actor_list = []

    # Upload objects under const.RANGE_MAX (Leave close proximity objects to allow them to block)
    for s in shadow_list:
        robot_to_object = s.get_position() - robot_position

        if in_camera_view(camera_direction, robot_to_object):

            # Check if object is further than view range
            dist = np.linalg.norm(robot_to_object)
            if dist <= const.RANGE_MAX:
                # Angle range for dismissing objects behind objects
                dir_vec = robot_to_object
                delta_theta = math.atan(s.get_radius()/dist)

                # Add to in_view array
                in_view.append(s)
                angle_ranges.append([dir_vec, delta_theta])

            # Hold onto distance values less than const.RANGE_MIN for future removal
            if dist < const.RANGE_MIN:
                # Use in dismissals
                in_close_proximity.append(s)

        # populate shadow actor list
        if s.mirrored:
            shadow_actor_list.append(s)
            print "Added to shadow_actor_list!"

    # Dismiss shadow objects behind mirrored shadow objects   ----------------- Front OBJECT MUST BE IN ACTOR LIST
    # Check for angle overlaps ( Permute ) - Tested
    view_blocked = []

    for v1i in range(0, len(in_view)-1):
        for v2i in range(v1i + 1, len(in_view)):

            v1 = angle_ranges[v1i][0]
            v2 = angle_ranges[v2i][0]

            # radius blocked angle
            blocked_theta_v1 = angle_ranges[v1i][1]
            blocked_theta_v2 = angle_ranges[v2i][1]

            # get magnitudes
            d_v1 = np.linalg.norm(v1)
            d_v2 = np.linalg.norm(v2)

            #  get angle
            cos_angle_between = np.dot(v1, v2)/(d_v1 * d_v2)

            if cos_angle_between > 1:
                print "Error: cos_angle_between is greater than 1: " + str(cos_angle_between)
                print "I'll set it to 1"
                cos_angle_between = 1
            elif cos_angle_between < -1:
                print "Error: cos_angle_between is less than -1: " + str(cos_angle_between)
                print "I'll set it to -1"
                cos_angle_between = -1
            # get angle
            angle_between = math.acos(cos_angle_between)

            # Remove if angle is less than sum of blockage (angles overlap)
            if angle_between < blocked_theta_v1 + blocked_theta_v2:
                # print "objects: " + str(v1) + " and " + str(v2) + " overlap"

                # Find which obj is in front
                # v1 is further from robot than v2
                if d_v1 > d_v2:
                    if in_view[v1i] not in view_blocked:
                        # check if front object(v2 is mirrored)
                        if in_view[v2i].mirrored:
                            view_blocked.append(in_view[v1i])
                else:
                    if in_view[v2i] not in view_blocked:
                        # check if front object(v1 is mirrored)
                        if in_view[v1i].mirrored:
                            view_blocked.append(in_view[v2i])

    # remove view_blocked list from view
    for r in view_blocked:
        # print "Removing -- Id: " + str(id(r)) + ", Object type: " + str(r.actor_type) + ", Position: " + str(r.get_position())
        in_view.remove(r)
        print "Removing what is blocked from view"

    # remove objects from view that are closer than const.RANGE_MIN
    for v in in_view:
        if v in in_close_proximity:
            in_view.remove(v)
            print "Removing what is too close"

    # in_view? then detected_list.
    pairs = []

    # Key:
    # Physical: detected obj
    # Digital: DOM virtual
    # Pair: [digital, physical] <- physical in digital radius

    # deep copy digitals and physicals (not too deep)
    unpaired_digitals = []
    for i in range(0, len(in_view)):
        unpaired_digitals.append(in_view[i])

    unpaired_physicals = []
    for i in range(0, len(detected_list)):
        unpaired_physicals.append(detected_list[i])

    # Pair Objects

    # Check all combinations of 2
    for si in range(0, len(in_view)):
        for di in range(0, len(detected_list)):

            # Find if each detected object is inside a radius sphere (will only be in one sphere, see cond. 3)
            # get the radius to each object (should only find one pair)
            # radius must not overlap (merge)
            distance_to_detected = np.linalg.norm(in_view[si].get_position() - detected_list[di].get_position())
            in_radius = distance_to_detected < in_view[si].get_radius()
            same_type = in_view[si].actor_type == detected_list[di].actor_type

            if in_radius and same_type:
                # print "PAIRING: In view at " + str(in_view[si].get_position()) + " with detected at " + str(detected_list[di].get_position())
                pair = Pair(in_view[si], detected_list[di])
                pairs.append(pair)

                # remove from unpaired lists
                if pair.digital in unpaired_digitals:
                    unpaired_digitals.remove(pair.digital)
                if pair.physical in unpaired_physicals:
                    unpaired_physicals.remove(pair.physical)

                # NEW- Allowed to pair multiple physicals to the same digital
                # break

    # Verify 1 to 1 paring (REMOVE IN FINAL VERSION)
    error_flag = 0

    # check physicals
    for p in pairs:

        identical_physicals = 0
        for c in pairs:
            if p.physical is c.physical:
                identical_physicals += 1

        if identical_physicals != 1:
            print "point to object pairing is broken (multiple physicals), "
            print str(identical_physicals) + " identical physicals exist for obj: " + str(id(p))
            error_flag = 1

    # update unpaired as missing (lower the probability)
    for m in unpaired_digitals:
        m.update_missing(robot_position)

    # update paired
    for p in pairs:
        # update and re-merge
        # (re-merge consolidates overlapped probability spheres)
        p.digital.update(p.physical.get_position(), robot_position)
        p.digital.merge_in(actor_list, shadow_list)

    # sanitize unpaired_physicals
    dismiss_list = []

    # remove physical objects closer than const.RANGE_MIN
    for p in unpaired_physicals:
        v1 = p.get_position() - robot_position
        d_v1 = np.linalg.norm(v1)
        if d_v1 < const.RANGE_MIN:
            if p not in dismiss_list:
                dismiss_list.append(p)

    # remove unpaired physical objects behind actors (Duplicates code of the blocked_view array) -- Modularize
    for a in shadow_actor_list:
        for p in unpaired_physicals:

            v1 = a.get_position() - robot_position
            v2 = p.get_position() - robot_position

            theta_v1 = math.atan(a.get_radius() / dist)
            theta_v2 = math.atan(p.get_radius() / dist)

            # get magnitudes
            d_v1 = np.linalg.norm(v1)
            d_v2 = np.linalg.norm(v2)

            #  get angle
            cos_angle_between = np.dot(v1, v2) / (d_v1 * d_v2)

            if cos_angle_between > 1:
                print "Error: cos_angle_between is greater than 1: " + str(cos_angle_between)
                print "I'll set it to 1"
                cos_angle_between = 1
            elif cos_angle_between < -1:
                print "Error: cos_angle_between is less than -1: " + str(cos_angle_between)
                print "I'll set it to -1"
                cos_angle_between = -1

            # get angle
            angle_between = math.acos(cos_angle_between)

            # Remove if angle is less than sum of angles (angles overlap)
            if angle_between < theta_v1 + theta_v2:
                # if actor is in front of p, remove p
                # Note: p is not within any radius or else it would have been paired
                if d_v1 < d_v2:  # v1 = a & v2 = p
                    if p not in dismiss_list:
                        dismiss_list.append(p)

    # remove physicals in list -- rename to view_blocked
    for d in dismiss_list:
        unpaired_physicals.remove(d)

    # sanitation complete

    # create objects not paired physicals
    for n in unpaired_physicals:
        # check if in range
        dist = np.linalg.norm(n.get_position() - robot_position)
        if const.RANGE_MIN < dist < const.RANGE_MAX:

            # create and add to list
            new_shadow_obj = ShadowObj(n.get_actor_type(), n.get_position(), robot_position)
            shadow_list.append(new_shadow_obj)

            # merge overlaps
            new_shadow_obj.merge_in_new(actor_list, shadow_list)

    # toggle everything in_view
    for s in in_view:
        # print "ID in toggle updater: " + str(id(s))
        s.toggle_mirrored(world, actor_list, shadow_list) #detected_list)


def in_camera_view(camra_dir, object_dir):
    return True

# Precise divide
# a/b with precision
# def precise_divide(a, b, precision_bits):
#     a_int = int(a)
#     b_int = int(b)
#     a_size = a_int.bit_length()
#     b_size = b_int.bit_length()
#     if (a_size <= 2*precision_bits) or (b <= precision_bits):
#         return a/b
#     a_temp = a_int >> (a_size - 2*precision_bits)
#     b_temp = b_int >> (b_size - precision_bits)
#     #temp = int(a) << int(precision_bits)
#     #r = temp // b
#     r = a_temp/b_temp
#     return r / 2**precision_bits


