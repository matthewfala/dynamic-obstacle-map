# Can we remove this file in our final version? -Matt

import numpy as np
import math
def rotate(vector,theta):
    r = np.array([[math.cos(theta), math.sin(theta),0],[-math.sin(theta), -math.cos(theta),0],[0,0,1]])
    print(r)
    return vector.dot(r)
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))   
def direction(position,target,orientation,vel,acc,w,a,t,max_angle,max_magn):
    if(np.linalg.norm(np.subtract(position,target))<.005):
        acc = vel/t
    if(abs(position[2]-target[2])>.05):
        #desire = target[2]-position[2]
        #return np.clip(np.array([0,0,1])*(desire-vel[2]),-max_magn,max_magn),0
        
        if vel[2] == 0:
             return np.clip(np.array([0,0,1])*(target[2]-position[2])*max_magn,-max_magn,max_magn),0
        distance = target[2]-position[2]
        exp_t = distance / vel[2]
        if exp_t < 0:
            return np.clip(np.array([0,0,1])*(target[2]-position[2])*max_magn,-max_magn,max_magn),0
        if vel[2] - math.pow((exp_t-t),2) * max_magn * (-1 if vel[2] > 0 else 1):
            return np.clip(np.array([0,0,1])*2*(distance - vel[2]*exp_t)/math.pow(exp_t,2),-max_magn,max_magn),0
    acc[2] =vel[2]/-t 
    desire = np.subtract(target[0:2],position[0:2])
    a = 0;
    acc[0:2] = np.clip(np.subtract(desire,vel[0:2]),-max_magn,max_magn)
    return (acc,a)
#position is absolute
#orientation is an angle

def update(position,orientation,vel,acc,w,a,t):
    orientation =orientation -(w * t + .5 * a* t * t)     
    position = position + t * vel + .5* t * t * acc
    return (position,orientation,vel + t * acc)
pos = np.array([0,0,3])
vel = np.array([0,0,0])
acc = np.array([0,0,0])
w = 0
a = 0
orientation = 0
max_angle = math.pi
max_magn = 1
target = np.array([10,0,57.53])
t = 1
i =0 
while(np.linalg.norm(np.subtract(pos,target)) > 0.0005 or np.linalg.norm(vel) >0.005):
    print('step:{3} position:{0}, velocity:{2} and score:{1}'.format(pos,np.linalg.norm(np.subtract(pos,target)),vel,i))
    acc,a = direction(pos,target,orientation,vel,acc,w,a,t,max_angle,max_magn)
    pos, orientation,vel = update(pos,orientation,vel,acc,w,a,t)
    i = i +1 
print('step:{3} position:{0}, velocity:{2} and score:{1}'.format(pos,np.linalg.norm(np.subtract(pos,target)),vel,i))



