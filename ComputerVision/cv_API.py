from Queue import Queue
from threading import Thread

"""
List of classes:

bin
bin_cover
buoy_green
buoy_red
buoy_yellow
channel
object_dropoff
object_pickup
path_marker
qual_gate
gate_pole
torpedo_cover
torpedo_hole
torpedo_target
"""
# Item has the following
#     string name
#     double score
#     double distance
#     double time detected
#     double time for frame

class Item:
     def __init__(self, name, score, distance, frame_time, detect_time):
           self.name = name
           self.score = score #0 to 100
           self.distance = distance
           self.frame_time = frame_time
           self.detect_time = detect_time

# This class was taking the parameters for creating an item and creating
# it to push into the queue
# Might not need this class
# Instead we can create a queue in a shared thread and push and pull items
# from there

# class Item_Q:
#
#     def __init__(self):
#         self.queue = Queue()
#
#     def push(self, name, score, distance, frame_time, detect_time):
#         temp = Item(name, score, distance, frame_time, detect_time)
#         self.queue.put(temp)
#
#
#     def pull():
#         temp = self.queue.get()
#         return temp
#
