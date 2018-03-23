import time

import pathplanner as pp

class NavSystem:
  def __init__(self):
    #Initialize World

    self.planner = pp.PathPlanner()

    self.ticks = 0
    self.__UPDATES_PER_SECOND = 5.0
    self.__TICK_DURATION = 1 / self.__UPDATES_PER_SECOND
    self.__SYNC_TICK_TIME = 1
    
  def run(self):
   #Start the main loop
   isOnline = True
   nextTickTime = time.time()
   previousTime = nextTickTime 
    
   while isOnline:
    
     if time.time() > nextTickTime:
        self.ticks += 1
        currentTime = time.time() 
        if self.ticks > self.__SYNC_TICK_TIME:
          self.update(currentTime - previousTime)
        previousTime = currentTime 
        nextTickTime += self.__TICK_DURATION
 
  def update(self, deltaT):
      print "Updating Tick #: " +  str(self.ticks) + " with DeltaT= " + str(deltaT)
      self.planner.update(deltaT)

navSystem = NavSystem()
navSystem.run()
