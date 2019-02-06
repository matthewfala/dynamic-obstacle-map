###############################
#       Simulation.py         #
#       By Matthew Fala       #
###############################

# Description: Simulates an AUV flyby past the simulation_world's obstacle set. Velocity and position
# are all updated.

# Usage: Test the DOM (Dynamic Obstacle Map. Run this script to test dom.py


# Import Dynamic Obstacle Map
import dom
import simulation_world as sw
import numpy as np
import time

# Setup fake world and robot
robot_position = np.array([-5.0, -5.0, -5.0])
v = np.array([0, 0, 0])
camera_direction = np.array([0, 0, 0])
actor_list = []
my_shadow_list = []
world = sw.DumbWorld(actor_list)


# $$$$$$$$$$$$$$$$$$$$ SIMULATION $$$$$$$$$$$$$$$$$$$$$$$$$
if True:
    # run timed simulation
    test_cycles = 10000

    mytime = 0
    dt = .2
    ctr = 0

    # Mark Time
    start_time = time.clock()

    for i in range(0, test_cycles):

        detected_list = sw.get_detected_list(robot_position, sw.fake_coords)
        dom.update_actors(world, camera_direction, robot_position, actor_list, my_shadow_list, detected_list)

        dx = np.multiply(v, dt)
        robot_position += dx
        print str(ctr) #+  "########################################################################################################################################################"
        print " "
        print "~~Robot~~Position~~~~~~~~~~~~~~" + str(robot_position.item(0)) + ", " + str(robot_position.item(1)) + ", " + str(robot_position.item(2)) + " ~~~~"
        print "~~ShadowList~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        for s in my_shadow_list:
            print "Shadow -- " + str(id(s)) + " -- Actor type: " + str(s.actor_type) + " -- At: " + str(s.get_position().item(0)) + ", " + str(s.get_position().item(1)) + ", " + str(s.get_position().item(2)) + " --Probability " + str(s.probability) + " -- Probe " + str(s.probed) + " -- Mirrored: " + str(s.mirrored)
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "~~ActorList~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        for s in actor_list:
            print "Actor -- " + str(id(s)) + " -- Actor type: " + str(s.actor_type) + " -- At: " + str(s.get_position().item(0)) + ", " + str(s.get_position().item(1)) + ", " + str(s.get_position().item(2))
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

        time.sleep(dt)
        mytime += dt
        ctr += 1

        if ctr == 10:
            sw.fake_coords.append(["buoy", np.array([-3, -3.0, -3.0])])
            sw.fake_coords.append(["buoy", np.array([-2, -3.0, -2.0])])
            # fake_coords.append(["buoy", np.array([3, 3, 3])])

        if ctr == 20:
            robot_position = np.array([-3.3, -3.3, -3.3])


# $$$$$$$$$$$$$$$$$$$$ TIMED TEST $$$$$$$$$$$$$$$$$$$$$$$$$
if False:

    # run timed simulation
    test_cycles = 10000

    dt = .4
    ctr = 0

    # mark start time
    start_time = time.clock()

    for i in range(0, test_cycles):
        detected_list = sw.get_detected_list(robot_position, sw.fake_coords)
        dom.update_actors(world, camera_direction, robot_position, actor_list, my_shadow_list, detected_list)

        v = np.array([.5, .5, .5])
        dx = np.multiply(v, dt)
        robot_position += dx

    # mark time
    end_time = time.clock()
    time_elapsed = end_time - start_time

    # measure time used for the random input creation
    start_time = time.clock()
    for i in range(0, test_cycles):
        detected_list = sw.get_detected_list(robot_position, sw.fake_coords)
    random_list_time = end_time - start_time

    print "# --------------------------------------------------------------------------"
    print "# Updated World " + str(test_cycles) + " times in " + str(time_elapsed - random_list_time) + " seconds"
    print "# " + str((time_elapsed - random_list_time)/test_cycles) + " s/update"


