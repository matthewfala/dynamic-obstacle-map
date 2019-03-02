# CONSTANTS

# Position and hits are weighted by an exponent of 1 / view distance
EXP_WEIGHT = 5

# Error (meters) / Dist
# (Determines Error Sphere Radius)
VIEW_ERR = 0.1  # Also Valid: .2 #.5 / 7

MIN_VIEW_DIST_BUF = 1

# Attempt to only sense objects in range
RANGE_MIN = 1
RANGE_MAX = 20

# View ACTIVATE_VIEWS times before activating obj (v2.0 -- Possibly use for archiving)
ACTIVATE_VIEWS = 4

# Probabilities
CREATE_PROBABILITY = .5
REMOVE_PROBABILITY = .2
DESTROY_RECORD_PROBABILITY = .1


class ActorSetting:
    def __init__(self, actor_type, actual_radius):
        self.actor_type = actor_type
        self.actual_radius = actual_radius


# radius by the obstacles type
ActorSettings = [ActorSetting('buoy', .3)]
