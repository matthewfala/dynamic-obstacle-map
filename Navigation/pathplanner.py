from kordermath import kordermath as km
import numpy as np
from numpy.linalg import inv

class PathPlanner:

  def __init__(self):
    print "Initialized Path Planning System"
    self.currentTarget = km.vector(10, 5, 2)
    self.currentPosition = km.vector(0, 0, 0)
    self.timeToTarget = 5

    self.currentState = State( km.vector.zero(), km.vector.zero(), km.vector.zero() )
    self.targetState = State( self.currentTarget, km.vector.zero(), km.vector.zero() )

  def update(self, deltaT):
    print "Path Planner Time to go" + str(self.timeToTarget)
    #Get the next position current position, current target, time to target
    #Set current position = next position

    if self.timeToTarget > 0:
      self.currentState = self.getNextState(self.currentState, self.targetState, self.timeToTarget, deltaT)
      self.timeToTarget -= deltaT

    print self.currentState.position.x, self.currentState.position.y, self.currentState.position.z

  def getNextState(self, currentState, targetState, timeToTarget, dt):
    #For each dimension compute coefficient inverse to determine coefficients
    #Compute next step using quintic spline
    
    t = timeToTarget

    ######## A Matrix ########
    constraintMatrix = np.matrix([ [1, 0, 0,   0,     0,      0],
			           [0, 1, 0,   0,     0,      0],
			           [0, 0, 2,   0,     0,      0],
			           [1, t, t**2, t**3,  t**4,   t**5],
			           [0, 1, 2*t, 3*t**2, 4*t**3, 5*t**4],
			           [0, 0, 2,   6*t,   12*t**2, 20*t**3] ])
    in_constraintMatrix = inv(constraintMatrix)

    ######## X (constant) vector ########
    bx = np.matrix([ [currentState.position.x], [currentState.velocity.x], [currentState.acceleration.x],
                    [targetState.position.x], [targetState.velocity.x], [targetState.acceleration.x] ])
    by = np.matrix([ [currentState.position.y], [currentState.velocity.y], [currentState.acceleration.y],
                    [targetState.position.y], [targetState.velocity.y], [targetState.acceleration.y] ])
    bz = np.matrix([ [currentState.position.z], [currentState.velocity.z], [currentState.acceleration.z],
                    [targetState.position.z], [targetState.velocity.z], [targetState.acceleration.z] ])
  
    cx = in_constraintMatrix.dot(bx)
    cy = in_constraintMatrix.dot(by)
    cz = in_constraintMatrix.dot(bz)

    splineMatrix = np.matrix([ [1, dt, dt**2, dt**3,   dt**4,    dt**5],
                               [0, 1,  2*dt,  3*dt**2, 4*dt**3,  5*dt**4],
                               [0, 0,  2,     6*dt,    12*dt**2, 20*dt**3] ])

    xResult = splineMatrix.dot(cx)
    yResult = splineMatrix * cy
    zResult = splineMatrix * cz

    nextState = State(km.vector(xResult.item((0,0)), yResult.item((0, 0)), zResult.item((0,0))),
                      km.vector(xResult.item((1,0)), yResult.item((1, 0)), zResult.item((1,0))),
                      km.vector(xResult.item((2,0)), yResult.item((2, 0)), zResult.item((2,0))))

    return nextState 


class State:

  def __init__(self, position, velocity, acceleration):
    self.position = position # already a km.vector when passing in
    self.velocity = velocity
    self.acceleration = acceleration


