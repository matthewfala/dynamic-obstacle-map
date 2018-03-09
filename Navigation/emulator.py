import numpy as np
import math
import world

class Emulator:
    ''' Emulation the real world

                    +-> Environment +-+
                    |    (Emulator)   |
             Action |                 | Observation
                    |                 |
                    +----+ Agent <----+

    1. Eable the interaction between the "simulated real world" and our intelligent nav system.
    2. The realworld information will be used for visualization.
    3. The 'observation' will be represented in the form what CV team can give, and info from sensors.

    Attributes:
        realworld: an instance of class World, contains real information of actors.
        initial_file: the file where we get initial states of actors.
        out_file: the file where we write the info of actors for visualization.

    Interfaces:
        reset(self): reset the environment, return 'observation'.
        step(self, action):
            push forward a timestep, return 'observation' and information
            related to tasks, like whether reached the destination.
        world_info(self, out_file): write the info of actors to a file for visualization.
    '''

    realworld = None
    initial_file = None
    out_file = None


    def __init__(self, initial_file, out_file):
        '''
        Initial the position of actors in realworld.
        Args:
            initial_file: get the initial states info from file.
        '''
        self.realworld = world.World()
        self.initial_file = initial_file
        self.out_file = out_file
        reset()

    def reset(self):
        '''
        Reset the environment to initial states
        '''
        # TODO: clear the world and add initial actors
        # realworld.clear()
        # realworld.create_actor(self, actorType, position)

    def step(self, action):
        '''
        For emulation, call by nav system.
        Args:
            action: the control signals of robot, or just the kinetic information at the first stage.
        Return:
            robot's direction
            camera's direction
            objects position from CV team
            sensor parameters (optional)
        '''
        # TODO

    def world_info(self):
        '''
        Write the actors' information out_file for visualization
        '''
        # TODO
