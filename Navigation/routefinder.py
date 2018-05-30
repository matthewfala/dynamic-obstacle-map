


class Path:

    def __init__(self, planning_mode, obstacles, start_point, end_point):
        if planning_mode in "astar_oct,astar_roadmap,dstar_oct,dstar_roadmap":
            self.planning_mode = planning_mode
        else:
            print "Error: using unsupported planning_mode in routefinder.py"
            return
        self.obstacle_set = set(obstacles)
        self.start = start_point
        self.end = end_point

#Store nodes in heap queue
class Node:
    def __init__(self, x, y, z, parent_node):

