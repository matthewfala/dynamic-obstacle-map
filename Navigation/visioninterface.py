import numpy as np
import math
import random
import time
#from msvcrt import getch # for keyboard controls

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
ACTIVATE_VIEWS = 10

# Probabilities
CREATE_PROBABILITY = .5
REMOVE_PROBABILITY = .2
DESTROY_RECORD_PROBABILITY = .1

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
def update_actors(world, camera_direction, robot_position, actor_list, shadow_list, detected_list):

    # Find all objects in shadow_list that should be updated
    in_view = [] # contains shadow object, and angle range

    angle_ranges = []

    # Upload objects within range
    for s in shadow_list:
        robot_to_object = s.get_position() - robot_position

        if in_camera_view(camera_direction, robot_to_object):

            # Check if object is within within view range
            dist = np.linalg.norm(robot_to_object)
            if RANGE_MIN < dist < RANGE_MAX:

                # Angle range for dismissing objects behind objects
                dir_vec = robot_to_object
                delta_theta = math.atan(s.get_radius()/dist)

                # Add to in_view array
                in_view.append(s)
                angle_ranges.append([dir_vec, delta_theta])


    # Dismiss shadow objects behind other shadow objects  ----------------- Front OBJECT MUST BE ACTOR LIST
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

            #  get angle
            cos_angle_between = np.dot(v1, v2)/(d_v1 * d_v2);

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
                #print "objects: " + str(v1) + " and " + str(v2) + " overlap"

                # Find which obj is in front
                # v1 is further from robot than v2
                if d_v1 > d_v2:
                    if in_view[v1i] not in dismiss_list:
                        dismiss_list.append(in_view[v1i])
                else:
                    if in_view[v2i] not in dismiss_list:
                        dismiss_list.append(in_view[v2i])

    # remove dismiss list from view
    #print "Removing from view: "
    for r in dismiss_list:
        # print "Removing -- Id: " + str(id(r)) + ", Object type: " + str(r.actor_type) + ", Position: " + str(r.get_position())
        in_view.remove(r)

    # in_view, then detected_list
    pairs = []

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

            # get the radius to each object ( should only find one pair )
            # radius must not overlap
            #print "Trying to pair: In view at " + str(in_view[si].get_position()) + " with detected at " + str(detected_list[di].get_position())
            distance_to_detected = np.linalg.norm(in_view[si].get_position() - detected_list[di].get_position())
            #print "id: " + str(id(detected_list[di])) + ", Distance to: " + str(distance_to_detected) + ", Radius : " + str(in_view[si].get_radius())
            if distance_to_detected < in_view[si].get_radius():
                print "PAIRING: In view at " + str(in_view[si].get_position()) + " with detected at " + str(detected_list[di].get_position())
                pair = Pair(in_view[si], detected_list[di])
                pairs.append(pair)

                # remove from unpaired lists
                unpaired_digitals.remove(pair.digital)
                unpaired_physicals.remove(pair.physical)

                # move onto next shadow(digital) object
                break

    # Verify 1 to 1 paring (REMOVE IN FINAL VERSION)

    error_flag = 0

    # check physicals
    for p in pairs:

        identical_digitals = 0
        for c in pairs:
            if p.digital is c.digital:
                identical_digitals += 1

        if identical_digitals != 1:
            print "1 to 1 radius pairing broken (multiple digitals), "
            print str(identical_digitals) + " identical digitals exist for obj: " + str(id(p))
            error_flag = 1

    # check physicals
    for p in pairs:

        identical_physicals = 0
        for c in pairs:
            if p.physical is c.physical:
                identical_physicals += 1

        if identical_physicals != 1:
            print "1 to 1 radius pairing broken (multiple physicals), "
            print str(identical_physicals) + " identical physicals exist for obj: " + str(id(p))
            error_flag = 1

    # permute should take care of multiple pairs
    # check mix

    # for p in pairs:
    #     identical = 0
    #     for c in pairs:
    #         if p.physical is c.digital:
    #             identical += 1
    #
    #     if identical != 1:
    #         print "1 to 1 radius pairing broken(permutation), "
    #         print str(identical) + " identical exist for obj: " + str(id(p))
    #         error_flag = 1
    #
    # # exit if errors occur
    # if error_flag:
    #     return 1

    # now each pairs are definitely 1 to 1

    # find missing
    #for v in in_view:
    #    found = 0
    #    for p in pairs:
    #        if p.digital is v:
    #            found = 1
                #break
    #    if not found:
    #        missing.append(v)

    # update unpaired as missing
    for m in unpaired_digitals:
        m.update_missing(robot_position)

    # update paired
    for p in pairs:
        # update and re-merge
        p.digital.update(p.physical.get_position(), robot_position)
        p.digital.merge_in(actor_list, shadow_list)

    # create objects not paired
    print "~~ Creating New Objects ~~"
    for n in unpaired_physicals:
        # check if in range
        dist = np.linalg.norm(n.get_position() - robot_position)
        if RANGE_MIN < dist < RANGE_MAX:

            # create and add to list
            new_shadow_obj = ShadowObj(n.get_actor_type(), n.get_position(), robot_position)
            shadow_list.append(new_shadow_obj)

            # merge overlaps
            new_shadow_obj.merge_in(actor_list, shadow_list)

    # toggle everything in_view
    for s in in_view:
        print "ID in toggle updater: " + str(id(s))
        print str(s in shadow_list)
        s.toggle_mirrored(world, actor_list, shadow_list) #detected_list)

def in_camera_view(camra_dir, object_dir):
    return True


class ActorSetting:
    def __init__(self, actor_type, actual_radius):
        self.actor_type = actor_type
        self.actual_radius = actual_radius


# radius by the obstacles type
ActorSettings = [ActorSetting('buoy', .3)]


class ShadowObj:

    # probability of existance
    probability = 1

    # number of times obj should be in view
    probed = 0

    type_settings = None

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
    sum_r_weight = 0

    error_radius = 0
    actual_radius = 0

    mirrored = False
    mirror_actor = None

    def __init__(self, actor_type, position, robot_position):

        self.actor_type = actor_type
        for s in ActorSettings:
            if s.actor_type == self.actor_type:
                #self.type_settings = s
                self.actual_radius = s.actual_radius

        # give weight to find
        distance = np.linalg.norm(position-robot_position)
        #print "DISTANCE TO OBJECT: " + str(distance)

        # update position (increments sum_weight and sum_found)
        self.update_position(position, robot_position)

        # update radius
        self.update_radius(distance)

        # min_view_dist and radius
        self.min_view_distance = distance

        #self.sum_r_err += self.get_radius(self.min_view_distance) * weight

        # increment probed
        self.probed += 1

        print "Id: " + str(id(self)) + ", Object type: " + str(self.actor_type) + ", Position: " + str(self.get_position()) # + ", Distance Viewed: " + self.distance

    # If the object is known to be viewed, probe
    #def probe(self, detected_pos, view_distance):

    def merge_in(self, actor_list, shadow_list):
        print "Merge Called"
        for l in shadow_list:
            if l is not self:
                # check for overlaps
                dist_between = np.linalg.norm(self.get_position() - l.get_position())
                if dist_between < (self.get_radius() + l.get_radius()):

                    # check who has more priviledge

                    # l has more privledge
                    if l.get_sum_found() > self.get_sum_found():
                        # update only if the radius is smaller
                        if l.get_radius() < self.get_radius():
                            # merge position
                            m_pos = self.get_position()
                            l.sum_x += self.sum_x #m_pos.item(0)
                            l.sum_y += self.sum_y #m_pos.item(1)
                            l.sum_z += self.sum_z #m_pos.item(2)
                            l.sum_weight += self.get_sum_weight()
                            l.sum_found += self.get_sum_found()
                            l.refresh_position()

                            # merge radius
                            l.sum_r_err += self.sum_r_err
                            l.sum_r_weight += self.sum_r_weight
                            l.refresh_radius()

                        # delete self # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WILL CAUSE PROBLEMS FOR UPDATING
                        self.safe_remove(actor_list, shadow_list)

                        # call merge_in on l
                        l.merge_in(actor_list, shadow_list)

                    # self has more privledge
                    else:
                        # update only if the radius is smaller
                        if self.get_radius() < l.get_radius():
                            # merge position
                            m_pos = l.get_position()
                            self.sum_x += l.sum_x #m_pos.item(0)
                            self.sum_y += l.sum_y #m_pos.item(1)
                            self.sum_z += l.sum_z #m_pos.item(2)
                            self.sum_weight += l.get_sum_weight()
                            self.sum_found += l.get_sum_found()
                            self.refresh_position()

                            # merge radius
                            self.sum_r_err += l.sum_r_err
                            self.sum_r_weight += l.sum_r_weight
                            self.refresh_radius()

                        # delete l  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WILL CAUSE PROBLEMS FOR UPDATING WORLD
                        l.safe_remove(actor_list, shadow_list)

                        # call merge_in on new merged obj (incase overlapping new obj)
                        self.merge_in(actor_list, shadow_list)

                    break

    def get_position(self):
        return self.position

    def get_radius(self):
        if self.actual_radius > self.error_radius:
            return self.actual_radius
        else:
            return self.error_radius

    def get_sum_found(self):
        return self.sum_found

    def get_sum_weight(self):
        return self.sum_weight

    def update(self, position, robot_position):
        distance = np.linalg.norm(position - robot_position)

        # update if the new radius is smaller or within min_view_dist_buf
        if self.get_radius_error(distance - MIN_VIEW_DIST_BUF) < self.get_radius():
            self.update_position(position, robot_position)
            self.update_radius(distance)
            # update probability
            self.probability = self.sum_weight/self.sum_found
            self.probed += 1

    def update_missing(self, robot_position):
        dist = np.linalg.norm(self.get_position()-robot_position)
        print "Missing Object -- id: " + str(id(self))
        self.sum_found += self.dist_weight(dist)
        self.probability = self.sum_weight / self.sum_found
        self.probed += 1

    def update_position(self, position, robot_position):

        # distance to new position of updater object
        dist = np.linalg.norm(position - robot_position)
        #print "PROBLEM DISTANCE TO OBJECT: " + str(dist)
        weight = self.dist_weight(dist)

        # give initial position
        self.sum_x += position.item(0) * weight
        self.sum_y += position.item(1) * weight
        self.sum_z += position.item(2) * weight
        self.sum_weight += weight

        # compute new position array
        self.position = np.array([self.sum_x/self.sum_weight, self.sum_y/self.sum_weight, self.sum_z/self.sum_weight])
        self.sum_found += weight

    def refresh_position(self):
        self.position = np.array([self.sum_x / self.sum_weight, self.sum_y / self.sum_weight, self.sum_z / self.sum_weight])
        self.probability = self.sum_weight / self.sum_found

    # provide distance and weight, and it will adjust radius
    def update_radius(self, distance):
        # use standard dist_weight as weight
        weight = self.dist_weight(distance)
        self.sum_r_weight += weight
        # increment radius
        self.sum_r_err += self.get_radius_error(distance) * weight
        # update error_radius
        self.error_radius = self.sum_r_err/self.sum_r_weight

    def refresh_radius(self):
        self.error_radius = self.sum_r_err / self.sum_r_weight
        self.probability = self.sum_weight / self.sum_found

    def dist_weight(self, dist):
        if dist > RANGE_MIN:
            return dist * pow((RANGE_MAX/dist), EXP_WEIGHT)
        else:
            print "Error: Trying to divide by 0 or a negative in dist_weight() function"
            return 0

    #def get_radius_weight(self, dist):

    #def sighted(self, position):

    def get_radius_error(self, dist):
        return VIEW_ERR * dist

    def toggle_mirrored(self, world, _world_list, _shadow_list):
        print str(id(self)) + " Made it inside toggle_mirrored"
        if self.probed >= ACTIVATE_VIEWS:
            print str(id(self)) + " Made it inside toggle_mirrored Actions"

            if self.mirrored:
                if REMOVE_PROBABILITY < self.probability:
                    self.mirror_actor.update_position(self.position)
                elif DESTROY_RECORD_PROBABILITY < self.probability <= REMOVE_PROBABILITY:
                    # stop mirroring and remove from world
                    self.mirrored = False
                    if self in _world_list: _world_list.remove(self.mirror_actor) # POSSIBLY USE SAFER REMOVAL METHOD
                    self.mirror_actor = None
                elif self.probability <= DESTROY_RECORD_PROBABILITY:
                    self.mirrored = False
                    #print "Shadow List id: " + str(_)
                    print "Toggle~~Is " + str(id(self)) + " in Shadow_List: " + str(self in _shadow_list)
                    self.safe_remove(_world_list, _shadow_list)
                    self.mirror_actor = None

            else:
                if CREATE_PROBABILITY < self.probability:
                    self.mirror_actor = world.create_actor(self.actor_type, self.get_position())
                    print "Setting Mirrored Actor"
                    print self.mirror_actor
                    self.mirrored = True
                elif self.probability <= DESTROY_RECORD_PROBABILITY:
                    print "Destroying id: " + str(id(self)) + ". Probability: " + str(self.probability)
                    print "Toggle~~Is " + str(id(self)) + " in Shadow_List: " + str(self in _shadow_list)
                    self.safe_remove(_world_list, _shadow_list)

    def safe_remove(self, _world_list, _shadow_list):
        print "safe_remove contacted"
        if self.mirror_actor in _world_list:
            print "Attempting to remove from world"
            _world_list.remove(self.mirror_actor)

        print "Is " + str(id(self)) + " in Shadow_List: " + str(self in _shadow_list)
        if self in _shadow_list:
            _shadow_list.remove(self)
            if self in _shadow_list:
                print "REMOVAL FAILED"
        # remove from real world list! (maybe r.deleteActor(self)

    #def toggle_radius(self):
    #    if self.actual_radius > self.error_radius:
    #        self.radius = self.actual_radius
    #    else:
    #        self.radius = self.error_radius


# Create world lists
world_list = []

print "########## CREATING OBJECTS #####################"
#world_list.append(ShadowObj("buoy", np.array([5, 1, 0]), 10))
#world_list.append(ShadowObj("buoy", np.array([4, 0, 0]), 10))
#world_list.append(ShadowObj("buoy", np.array([2, 2, 0]), 6))
#world_list.append(ShadowObj("buoy", np.array([10, 2, 3]), 10))


#update_actors(np.array([2, 1, 0]), np.array([2.7, 0, 0]), world_list, world_list, [])

fake_coords = []
fake_coords.append(["buoy", np.array([5, 2, 3])])
fake_coords.append(["buoy", np.array([1, 2, 2])])
fake_coords.append(["buoy", np.array([6, 3, 1])])
fake_coords.append(["buoy", np.array([2, 5, 0])])
fake_coords.append(["buoy", np.array([2, 3, 1])])
fake_coords.append(["buoy", np.array([0, 1, 2])])

fake_error_per_dist = .05

def get_detected_list(robot_pos, fake_coords):
    detected_list = []
    for f in fake_coords:
        dist = np.linalg.norm(robot_pos-f[1])
        err = fake_error_per_dist * dist
        x = random.gauss(f[1].item(0), err)
        y = random.gauss(f[1].item(1), err)
        z = random.gauss(f[1].item(2), err)

        print "Random x y z generated: " + str(x) + ", " + str(y) + ", " + str(z)

        fake_pos = np.array([x, y, z])

        detected_list.append(DetectedObject(f[0], fake_pos))
    return detected_list


class DetectedObject():
    def __init__(self, _actor_type, _position):
        self.actor_type = _actor_type
        self.position = _position

    def get_actor_type(self):
        return self.actor_type

    def get_position(self):
        return self.position


class DumbWorld:
    def __init__(self, my_actor_list):
        self.actor_list = my_actor_list

    def create_actor(self, actorType, position):
        new_actor = DumbActor(actorType, position)
        self.actor_list.append(new_actor)
        return new_actor

class DumbActor:
    def __init__(self, actor_type, position):
        self.actor_type = actor_type
        self.position = position
    def get_position(self):
        return self.position
    def update_position(self, new_position):
        self.position = new_position

robot_position = np.array([0, 0, 0])
camera_direction = np.array([0, 0, 0])
actor_list = []
my_shadow_list = []

world = DumbWorld(actor_list)
# run simulation
while True:
    detected_list = get_detected_list(robot_position, fake_coords)
    update_actors(world, camera_direction, robot_position, actor_list, my_shadow_list, detected_list)
    #time.sleep(.5)
    print "~~Robot~~Position~~~~~~~~~~~~~~" + str(robot_position.item(0)) + ", " + str(robot_position.item(1)) + ", " + str(robot_position.item(2)) + " ~~~~"

    print "~~ShadowList~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    for s in my_shadow_list:
        print "Shadow -- " + str(id(s)) + " -- Actor type: " + str(s.actor_type) + " -- At: " + str(s.get_position().item(0)) + ", " + str(s.get_position().item(1)) + ", " + str(s.get_position().item(2)) + " --Probability " + str(s.probability) + " -- Probe " + str(s.probed) + " -- Mirrored: " + str(s.mirrored)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "~~ActorList~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    for s in actor_list:
        print "Actor -- " + str(id(s)) + " -- Actor type: " + str(s.actor_type) + " -- At: " + str(s.get_position().item(0)) + ", " + str(s.get_position().item(1)) + ", " + str(s.get_position().item(2))
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    # fake movement
    #if key == 80:  # Down arrow
    #    robot_position = np.subtract(robot_position + np.array[0,-.3,0])

    #elif key == 72:  # Up arrow
    #    robot_position = np.subtract(robot_position + np.array[0, .3, 0])







