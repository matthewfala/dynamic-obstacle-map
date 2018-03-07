import time

class NavSystem:
  def __init__(self):
    #Initialize World
    self.ticks = 0
    self.UPDATES_PER_SECOND = 5.0
    self.TICK_DURATION = 1 / self.UPDATES_PER_SECOND
    
  def run(self):
   #Start the main loop
   isOnline = True
   nextTickTime = time.time()
   previousTime = nextTickTime 
    
   while isOnline:
    
     if time.time() > nextTickTime:
        self.ticks += 1
        currentTime = time.time() 
        self.update(currentTime - previousTime)
        previousTime = currentTime 
        nextTickTime += self.TICK_DURATION
 
  def update(self, deltaT):
      print "Performing update after: " + str(deltaT)

navSystem = NavSystem()
navSystem.run()
