import kordermath
import numpy as np
import math

TURN_COST = 5
VERTICAL_COST = 10

class Path:
    def __init__(self, planning_mode, obstacles, start_point, end_point, nodes_per_meter):
        if planning_mode in "astar_oct,astar_roadmap,dstar_oct,dstar_roadmap":
            self.planning_mode = planning_mode
        else:
            print "Error: using unsupported planning_mode in routefinder.py"
            return
        self.obstacle_set = set(obstacles)
        self.open_heap = []  # this is a heap
        self.closed = set([])
        self.start = start_point
        self.end = end_point
        self.se = self.end - self.start
        self.nodes_per_meter = nodes_per_meter

        se_norm = np.linalg.norm(self.se)
        if se_norm == 0:
            print "Start and End nodes are the same. Path complete"
        else:
            se_normalized = self.se / se_norm
            self.ipath = se_normalized / self.nodes_per_meter
            self.jpath = np.array([-self.ipath.item(1), self.ipath.item(0), self.ipath.item(2)])
            self.kpath = np.array([0, 0, 1 / nodes_per_meter]) # in meter/node
            print self.ipath
            print self.jpath
            print self.kpath
        self.goal_node = np.array([math.floor(se_norm*nodes_per_meter), 0, math.floor(self.end * nodes_per_meter)])

    def get_node_coordinates(self, node):
        return np.array([node.a*self.ipath, node.b*self.jpath, node.c*self.kpath])

    def get_open_neighbors(self, node):
        pass

    def get_neighbor_h_cost(self, node):
        a_dist = self.goal_node.item(0) - node.a
        b_dist = self.goal_node.item(1) - node.b
        c_dist = self.goal_node.item(2) - node.c
        return math.sqrt(a_dist ** 2 + b_dist ** 2 + c_dist ** 2)


# Store nodes in heap queue
# <a, b, c> x <i, j, k>/resolution are the xyz coordinates
class Node:
    def __init__(self, a, b, c, parent_node, goal_node):
        self.a = a
        self.b = b
        self.c = c
        self.parent_node = parent_node
        self.cost = parent_node.cost + self.get_node_cost(self)  # this is the G(x) cost
        self.heuristic = self.get_node_heuristic(self, goal_node)

    def update_parent_node(self, parent_node, goal_node):
        self.parent_node = parent_node
        self.cost = parent_node.cost + self.get_node_cost(self)
        self.heuristic = self.get_node_heuristic(self, goal_node)

    # For node cost assignment
    @staticmethod
    def get_node_cost(node):
        dir_a = node.parent_node.a - node.parent_node.parent_node.a
        dir_b = node.parent_node.b - node.parent_node.parent_node.b
        dir_c = node.parent_node.c - node.parent_node.parent_node.c

        new_dir_a = node.a - node.parent_node.a
        new_dir_b = node.b - node.parent_node.b
        new_dir_c = node.c - node.parent_node.c

        # Cost assignment
        distance_cost = math.sqrt(new_dir_a ** 2 + new_dir_b ** 2 + new_dir_c ** 2)
        additional_cost = 0
        if dir_a == new_dir_a and dir_b == new_dir_b and dir_c == new_dir_c:
            additional_cost = 0
        elif dir_c == new_dir_c == 0:
            additional_cost = TURN_COST
        else:
            additional_cost = VERTICAL_COST

        return distance_cost + additional_cost

    @staticmethod
    def get_node_heuristic(node, goal_node):
        a_dist = goal_node.item(0) - node.a
        b_dist = goal_node.item(1) - node.b
        c_dist = goal_node.item(2) - node.c
        return math.sqrt(a_dist ** 2 + b_dist ** 2 + c_dist ** 2)


i = Path("astar_oct",[1,2,3], np.array([0,0,0]), np.array([5,5,3]), 5)
