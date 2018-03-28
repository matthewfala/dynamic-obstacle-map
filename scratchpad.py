import testmod
import numpy as np
import math
import time
from msvcrt import getch # for keyboard controls



class myanimal:
    name = "dog"

    def __init__(self, name):
        self.name = name


# animal list
mycat = myanimal('cat')
mydog = myanimal('dog')
animal = [mycat, mydog]

print("id of cat: ")
print(id(mycat))

this_obj = mycat

print("id of thisobj: ")
print(id(this_obj))

this_obj.name = "othercat"
print "id of othercat"
print id(this_obj)





print "ID of cat in function: " + str(testmod.get_id(this_obj))

print "name of cat: " + mycat.name

# 'rabbit' element is removed
#animal.remove(this_obj)




# Updated Animal List
print("updated list:")
for a in animal:
    print(a.name)

in_view = [0,1,2,3]
for s in range(0, len(in_view)-1):
    for comp in range(s + 1, len(in_view)):
        print(in_view[s])
        print(in_view[comp])

a = np.array([1,0,0])
b = np.array([0,1,0])
print np.linalg.norm(a)



# get magnitudes
d_v1 = np.linalg.norm(a)
d_v2 = np.linalg.norm(b)

# get angle
angle_between = math.acos(np.dot(a, b)/(d_v1 * d_v2))
print angle_between


# Euler vector rotation
# Ref pg 13 https://www.cs.utexas.edu/~theshark/courses/cs354/lectures/cs354-14.pdf
def euler_vector_rotate(v, alpha, beta, gamma):
    # Rotate about alpha
    x = v.item(0)
    y = v.item(1)
    z = v.item(2)
    v_alpha = np.array([x, y * math.cos(alpha) - z * math.sin(alpha), y * math.sin(alpha) + z * math.cos(alpha)])

    # Rotate about beta
    x = v_alpha.item(0)
    y = v_alpha.item(1)
    z = v_alpha.item(2)
    v_beta = np.array([x * math.cos(beta) + z * math.sin(beta), y, -x * math.sin(beta) + y * math.cos(beta)])

    # Rotate about gamma
    x = v_beta.item(0)
    y = v_beta.item(1)
    z = v_beta.item(2)
    v_gamma = np.array([x * math.cos(gamma) - y * math.sin(gamma), x * math.sin(gamma) + y * math.cos(gamma), z])

    #return fully rotated array
    return v_gamma


a = np.array([1, 0, 0])
print euler_vector_rotate(a, 0, 0, 3.141/2);

a = ["aloha", "mahalo"]

def removeAloha(b):
    b[0] = "not aloha"

removeAloha(a)
print a

while True:
    key = ord(getch())
    print key
    time.sleep(.5)

