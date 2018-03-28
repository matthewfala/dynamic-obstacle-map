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

# to connect detected with digital
class Pair:
    def __init__(self, digital, physical):
        self.digital = digital
        self.physical = physical

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
def update_actors(camera_direction, robot_position, actor_list, shadow_list, detected_list):

    # Find all objects in shadow_list that should be updated
    in_view = [] # contains shadow object, and angle range

    angle_ranges = []

    # Upload objects within range
    for s in shadow_list:
        robot_to_object = np.subtract(s.get_position(), robot_position)

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
        print "Id: " + str(id(r)) + ", Object type: " + str(r.actor_type) + ", Position: " + str(r.get_position)
        in_view.remove(r)

    # in_view, then detected_list
    pairs = []

    # deep copy digitals and physicals (not too deep)
    unpaired_digitals = []
    for i in range(0, len(in_view) - 1):
        unpaired_digitals[i] = in_view[i]
    unpaired_physicals = []
    for i in range(0, len(in_view) - 1):
        unpaired_physicals[i] = detected_list[i]

    # Pair Objects

    # permute
    for si in range(0, len(in_view)-1):
        for di in range(si + 1, len(detected_list)):
            # get the radius to each object ( should only find one pair )
            # radius must not overlap
            r = np.linalg.norm(in_view[si].get_position(), detected_list[di].get_position())
            if r < in_view[si].get_radius():
                pair = Pair(in_view[si], detected_list[di])
                pairs.append(pair)

                # remove from unpaired lists
                unpaired_digitals.remove(pair.digital)
                unpaired_physicals.remove(pair.physical)

    # Verify 1 to 1 paring (REMOVE IN FINAL VERSION)

    error_flag = 0

    # check physicals
    for p in pairs:
        identical_digitals = 0
        for c in pairs:
            if p.digital == c.digital:
                identical_digitals += 1
        if identical_digitals != 1:
            print "1 to 1 radius pairing broken (multiple digitals), "
            print str(identical_digitals) + " identical digitals exist for obj: " + str(id(p))
            error_flag = 1

    # check physicals
    for p in pairs:
        identical_physicals = 0
        for c in pairs:
            if p.physical == c.physical:
                identical_physicals += 1
        if identical_physicals != 1:
            print "1 to 1 radius pairing broken (multiple physicals), "
            print str(identical_physicals) + " identical physicals exist for obj: " + str(id(p))
            error_flag = 1

    # permute should take care of multiple pairs
    # check mix
    for p in pairs:
        identical = 0
        for c in pairs:
            if p.physical == c.digital:
                identical += 1
        if identical != 1:
            print "1 to 1 radius pairing broken(permutation), "
            print str(identical) + " identical exist for obj: " + str(id(p))
            error_flag = 1

    # exit if errors occur
    if error_flag:
        return 1

    # now each pairs are definitely 1 to 1

    # find missing
    #for v in in_view:
    #    found = 0
    #    for p in pairs:
    #        if p.digital == v:
    #            found = 1
                #break
    #    if not found:
    #        missing.append(v)

    # update unpaired objects as missing
    for m in unpaired_digitals:
        m.update_missing(robot_position)

    # update the rest at their current locations
    for p in pairs:
        # Update (may not update position if too close or far
        p.digital.update(p.physical.get_position(), robot_position)

    # create objects not paired (can edit shadow_list in function)
    for n in unpaired_physicals:
        # create the new object and add it to the list
        new_shadow_obj = ShadowObj(n.get_actor_type, n.position, robot_position)
        shadow_list.append(new_shadow_obj)
        # check if any overlaps exist and remove
        new_shadow_obj.merge_in(shadow_list)






# for d in detected_list:
        # Add if within min-view dist
   #     d_radius = VIEW_ERR * d.view_dist + MIN_VIEW_DIST_BUF


    #    if d.dist <


   # for a in in_view:


def in_camera_view(camra_dir, object_dir):
    return True





class ActorSetting:
    def __init__(self, actor_type, actual_radius):
        self.actor_type = actor_type
        self.actual_radius = actual_radius


# radius by the obstacles type
ActorSettings = [ActorSetting('buoy', .3)]


class ShadowObj:

    # number of times obj should be in view
    probed = 0

    # weighted finds
    sum_weight = 0 # weight is only added to if object should be seen
    sum_found = 0 # weight is added to regardless

    # weighted sums
    sum_x = 0
    sum_y = 0
    sum_z = 0

    # numpy position array
    position = np.array([0, 0, 0])

    # weighted radius sums by hit
    sum_r_err = 0
    error_radius = 0
    actual_radius = 0

    mirrored = False

    def __init__(self, actor_type, position, robot_position):

        self.actor_type = actor_type
        for s in ActorSettings:
            if s.actor_type == self.actor_type:
                self.type_settings = s

        # give weight to find
        distance = np.linalg.norm(position-robot_position)
        weight = self.dist_weight(distance)
        self.sum_weight += weight
        self.sum_found += weight

        # update position
        self.update_position(position, robot_position)

        # update radius
        self.actual_radius = self.type_settings.actual_radius
        self.update_radius(distance, weight)

        # min_view_dist and radius
        self.min_view_distance = distance

        #self.sum_r_err += self.get_radius(self.min_view_distance) * weight

        # increment probed
        self.probed += 1

        print "Id: " + str(id(self)) + ", Object type: " + str(self.actor_type) + ", Position: " + str(self.get_position()) # + ", Distance Viewed: " + self.distance

    # If the object is known to be viewed, probe
    #def probe(self, detected_pos, view_distance):

    def merge_in(self, list):
        for l in list:
            # check for overlaps
            dist_between = np.linalg.norm(self.get_position() - l.get_position())
            if (self.get_radius() + l.get_radius()) < dist_between:

                # merge only if radius is smaller
                # check who has more priviledge
                if (self.get_sum_found() > l.get_sum_found()):
                    m_pos = l.get_position()
                    mx = m_pos(0)
                    my = m_pos(1)
                    mz = m_pos(2)










    def get_position(self):
        return self.position

    def get_radius(self):
        if self.actual_radius > self.error_radius:
            return self.actual_radius
        else:
            return self.error_radius

    def get_sum_found(self):
        return self.sum_found

    def update(self, position, robot_position):
        distance = np.linalg.norm(position - robot_position)
        self.update_position(position, robot_position)

        # update if the new radius is smaller or within min_view_dist_buf
        if self.get_radius_error(distance - MIN_VIEW_DIST_BUF) < self.get_radius():
            self.update_radius(distance)

    def update_position(self, position, robot_position):

        dist = np.linalg.norm(self.get_position() - robot_position)
        weight = self.dist_weight(dist)

        # give initial position
        self.sum_x += position.item(0) * weight
        self.sum_y += position.item(1) * weight
        self.sum_z += position.item(2) * weight
        self.sum_weight += weight

        # compute new position array
        self.position = np.array([self.sum_x/self.sum_weight, self.sum_y/self.sum_weight, self.sum_z/self.sum_weight])
        self.sum_found += weight

    def update_missing(self, robot_position):
        dist = np.linalg.norm(self.get_position()-robot_position)
        self.sum_found += self.dist_weight(dist)

    # provide distance and weight, and it will adjust radius
    def update_radius(self, distance):
        # use standard dist_weight as weight
        weight = self.dist_weight(distance)
        # increment radius
        self.sum_r_err += self.get_radius_error(distance) * weight
        # update error_radius
        self.error_radius = self.sum_r_err/weight

    def dist_weight(self, dist):
        return dist * pow((RANGE_MAX/dist), EXP_WEIGHT)

    #def get_radius_weight(self, dist):

    #def sighted(self, position):

    def get_radius_error(self, dist):
        return VIEW_ERR * dist

    #def toggle_radius(self):
    #    if self.actual_radius > self.error_radius:
    #        self.radius = self.actual_radius
    #    else:
    #        self.radius = self.error_radius


# Create world lists
world_list = []

print "########## CREATING OBJECTS #####################"
world_list.append(ShadowObj("buoy", np.array([5, 1, 0]), 10))
world_list.append(ShadowObj("buoy", np.array([4, 0, 0]), 10))
world_list.append(ShadowObj("buoy", np.array([2, 2, 0]), 6))
world_list.append(ShadowObj("buoy", np.array([10, 2, 3]), 10))


update_actors(np.array([2, 1, 0]), np.array([2.7, 0, 0]), world_list, world_list, [])





