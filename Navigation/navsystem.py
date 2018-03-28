import time

import pathplanner as pp
import simwriter as simwriter

class NavSystem:
  def __init__(self):
    #Initialize World

    self.planner = pp.PathPlanner()
    self.writer = simwriter.SimWriter("ticks.json")

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
          isOnline = self.update(currentTime - previousTime)
        previousTime = currentTime 
        nextTickTime += self.__TICK_DURATION

   self.writer.writeFile()
 
  def update(self, deltaT):
      print "Updating Tick #: " +  str(self.ticks) + " with DeltaT= " + str(deltaT)
      self.planner.update(deltaT)
      self.writer.append(self.ticks, self.planner.currentState)
      #For testing only
      if self.ticks > 30:
         return False
      return True

navSystem = NavSystem()
navSystem.run()
