from multiprocessing import Process, Queue
from random import randint
import signal
import sys
import time

class AuvController(Process):
  def run(self):
    print 'Starting AUV process'
    self.initializeSystem()
    while True:
      print 'Doing AUV work...'
      time.sleep(.5)
 
  def initializeSystem(self):
    print 'AUV System initializing'

class NavigationSystem(Process):
  def run(self):
    print 'Starting Nav System Process'
    while True:
      print 'Checking course trajectory...'
      time.sleep(1)
      if (self.q):
        depth = self.q.get()
        print 'Received depth from message queue: ' + `depth`

  def initialize(self, q):
    print 'Nav System starting up...'
    self.q = q

class DepthSensor(Process):
  def run(self):
    print 'Starting depth sensor process.'
    while True:
      print 'Reading depth values...'
      time.sleep(.75)
      if (self.q):
        depthReading = randint(10, 100)
        self.q.put(depthReading)
 
  def initialize(self, q):
    print 'Depth Sensor starting...'
    self.q = q;

if __name__ == '__main__':
  #Create and start each subsystem process 
  mainController = AuvController()  
  mainController.start()

  #Create a shared message queue
  messageQueue = Queue()

  navSystem = NavigationSystem()
  navSystem.initialize(messageQueue)
  navSystem.start()

  depthSensor = DepthSensor()
  depthSensor.initialize(messageQueue) 
  depthSensor.start()
  
  #Create a handler that will be called when Ctrl-C is pressed
  def handle(signum, frame):
    print 'Attempting to handle signal...' 
    mainController.terminate()
    navSystem.terminate()
    depthSensor.terminate()
    print 'shutting down gracefully...'

  #Register the handler so we can propely terminate all processes 
  signal.signal(signal.SIGINT, handle) 
