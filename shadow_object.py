
import numpy as np
import settings as const


class ShadowObj:

    # probability of existence
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
        for s in const.ActorSettings:
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

        #print "Id: " + str(id(self)) + ", Object type: " + str(self.actor_type) + ", Position: " + str(self.get_position()) # + ", Distance Viewed: " + self.distance

    def merge_in_new(self, actor_list, shadow_list):
        for l in shadow_list:
            if l is not self:
                # check for same actor type
                same_type = self.actor_type == l.actor_type
                # check for overlaps
                dist_between = np.linalg.norm(self.get_position() - l.get_position())
                overlapping = dist_between < (self.get_radius() + l.get_radius())

                if same_type and overlapping:

                    # Self has the least credibility
                    # Merge over-rides -> just delete, self is smaller (when self r - r_distance_buf)
                    if l.get_radius() > (self.get_radius() - self.get_radius_error(const.MIN_VIEW_DIST_BUF)): # Works only for linear radius_error functions
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

                        # merge polls
                        l.probed += 1

                        print "Merged newly created"
                    else:
                        print "Chose to not merge newly created"

                    # delete self # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WILL CAUSE PROBLEMS FOR UPDATING
                    self.safe_remove(actor_list, shadow_list)

                    # call merge_in on l
                    l.merge_in(actor_list, shadow_list)

                    break

    def merge_in(self, actor_list, shadow_list):

        for l in shadow_list:
            if l is not self:
                # check for same actor type
                same_type = self.actor_type == l.actor_type
                # check for overlaps
                dist_between = np.linalg.norm(self.get_position() - l.get_position())
                overlapping = dist_between < (self.get_radius() + l.get_radius())

                if same_type and overlapping:
                    # check who has more credibility

                    # l has more credibility
                    if l.get_sum_found() > self.get_sum_found():
                        # update l only if the self radius is smaller
                        if l.get_radius() > self.get_radius():
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

                            # merge polls
                            l.probed += self.probed

                            print "Merge success"

                        else:
                            print "Merge failed, out of boundary"

                        # delete self # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WILL CAUSE PROBLEMS FOR UPDATING
                        self.safe_remove(actor_list, shadow_list)

                        # call merge_in on l
                        l.merge_in(actor_list, shadow_list)

                    # self has more credibility
                    else:
                        # update self only if l radius is smaller
                        if self.get_radius() > l.get_radius():
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

                            # merge polls
                            self.probed += l.probed

                            print "Merge Success"

                        else:
                            print "Merge failure"

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
        if self.get_radius_error(distance - const.MIN_VIEW_DIST_BUF) < self.get_radius():
            self.update_position(position, robot_position)
            self.update_radius(distance)

            # update probability
            self.probability = self.sum_weight/ self.sum_found
            self.probed += 1
        else:
            print "Could not update, out of range"

    def update_missing(self, robot_position):
        dist = np.linalg.norm(self.get_position()-robot_position)
        #print "Missing Object -- id: " + str(id(self))
        self.sum_found += self.dist_weight(dist)
        self.probability = self.sum_weight/self.sum_found
        self.probed += 1

    def update_position(self, position, robot_position):

        # distance to new position of updater object
        dist = np.linalg.norm(position - robot_position)
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
        # self.probability = self.sum_weight / self.sum_found

    def dist_weight(self, dist):
        if dist > const.RANGE_MIN:
            return dist * pow((const.RANGE_MAX/dist), const.EXP_WEIGHT)
        else:
            print "Error: Trying to divide by 0 or a negative in dist_weight() function"
            print "Devisor distance: " + str(dist)
            return 0

    #def get_radius_weight(self, dist):

    #def sighted(self, position):

    def get_radius_error(self, dist):
        return const.VIEW_ERR * dist

    def toggle_mirrored(self, world, _world_list, _shadow_list):
        #print str(id(self)) + " Made it inside toggle_mirrored"
        if self.probed >= const.ACTIVATE_VIEWS:
            #print str(id(self)) + " Made it inside toggle_mirrored Actions"

            if self.mirrored:
                if const.REMOVE_PROBABILITY < self.probability:
                    self.mirror_actor.update_position(self.position)
                elif const.DESTROY_RECORD_PROBABILITY < self.probability <= const.REMOVE_PROBABILITY:
                    # stop mirroring and remove from world
                    self.mirrored = False
                    if self in _world_list: _world_list.remove(self.mirror_actor) # POSSIBLY USE SAFER REMOVAL METHOD
                    self.mirror_actor = None
                elif self.probability <= const.DESTROY_RECORD_PROBABILITY:
                    self.mirrored = False
                    #print "Shadow List id: " + str(_)
                    #print "Toggle~~Is " + str(id(self)) + " in Shadow_List: " + str(self in _shadow_list)
                    self.safe_remove(_world_list, _shadow_list)
                    self.mirror_actor = None

            else:
                if const.CREATE_PROBABILITY < self.probability:
                    self.mirror_actor = world.create_actor(self.actor_type, self.get_position())
                    #print "Setting Mirrored Actor"
                    #print self.mirror_actor
                    self.mirrored = True
                elif self.probability <= const.DESTROY_RECORD_PROBABILITY:
                    #print "Destroying id: " + str(id(self)) + ". Probability: " + str(self.probability)
                    #print "Toggle~~Is " + str(id(self)) + " in Shadow_List: " + str(self in _shadow_list)
                    self.safe_remove(_world_list, _shadow_list)

    def safe_remove(self, _world_list, _shadow_list):
        #print "safe_remove contacted"
        if self.mirror_actor in _world_list:
            print "dd to remove from world"
            _world_list.remove(self.mirror_actor)

        #print "Is " + str(id(self)) + " in Shadow_List: " + str(self in _shadow_list)
        if self in _shadow_list:
            _shadow_list.remove(self)
            if self in _shadow_list:
                print "REMOVAL FAILED"


