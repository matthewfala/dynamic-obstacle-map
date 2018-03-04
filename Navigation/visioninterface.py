
# Constants

# Position and hits are weighted by an exponent of 1 / view distance
EXP_WEIGHT = 5

# Error (meters) / Dist
VIEW_ERR = .5 / 7

# View ACTIVATE_VIEWS times before activating obj
ACTIVATE_VIEWS = 100

# Probabilities
CREATE_PROBABILITY = .5
REMOVE_PROBABILITY = .2
DESTROY_RECORD_PROBABILITY = .05



# Create Shadow WorldT
shadow_list = []

class detected_obj:
    def __init__(self, view_dist, camera ):
        self.view_dist = view_dist
        self.angle =

def update_actors(actor_list, detected_list):

    # All objects that should be updated
    in_view = []

    for a in actor_list:
        for d in detected_list:
            d_radius =

    for a in in_view:





class shadow_obj:

    hits = 0

    # weighted sums by hit
    sum_x = 0
    sum_y = 0
    sum_z = 0

    in_view = 0
    mirrored = False

    def __init__ (self, type, position, dist):
        self.type = type
        self.position = position
        self.min_view_dist = dist
        self.radius = self.get_radius(self.view_dist)
        self.hits += 1
        self.in_view += 1

    def
    def sighted(self, position):

    def get_radius(self, dist):
        return VIEW_ERR * dist
e
