import numpy as np
from numpy import linalg as nla
from math import sin, cos, acos, sqrt

###########################################################################################
# KORDERMATH is the high level namespace for our Math Commons.
###########################################################################################
class KOrderMath:
    @classmethod
    def convert_degrees_to_radians(cls, degrees):
        return np.deg2rad(degrees)

    @classmethod
    def convert_radians_to_degrees(cls, degrees):
        return np.rad2deg(degrees)

    @classmethod
    def get_projection(cls, of_vector, on_vector):
        if not isinstance(of_vector, KOrderMath.Vector) or not isinstance(on_vector, KOrderMath.Vector):
            raise ValueError("You can only get projection of one KOrderMath.Vector on another KOrderMath.Vector")

        on_vector_mag = on_vector.magnitude()
        on_vector_norm = on_vector / on_vector_mag
        projection_comp = (of_vector % on_vector) / (on_vector_mag)
        projection = projection_comp * on_vector_norm
        return projection

    """
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

        # return fully rotated array
        return v_gamma
    """

    ###########################################################################################
    # VECTOR respresents a point or a direction in 3D space.
    # Our co-ordinate system will follow the convention:
    # X Axis is forward
    # Y Axis is right
    # Z Axis is up
    ###########################################################################################
    class Vector:
        def __init__(self, x, y, z):
            self.npvector = np.array([x, y, z])
            self.x = self.npvector[0]
            self.y = self.npvector[1]
            self.z = self.npvector[2]

        @classmethod
        def from_npvector(cls, npvector):
            return cls(npvector[0], npvector[1], npvector[2])

        def __add__(self, other):
            if not isinstance(other, KOrderMath.Vector):
                raise ValueError("You can only add a KOrderMath.Vector to another KOrderMath.Vector")

            return self.from_npvector(self.npvector + other.npvector)

        def __sub__(self, other):
            if not isinstance(other, KOrderMath.Vector):
                raise ValueError("You can only subtract a KOrderMath.Vector to another KOrderMath.Vector")

            return self.from_npvector(self.npvector - other.npvector)
        
        def __mul__(self, other):
            if isinstance(other, KOrderMath.Vector):
                return self.from_npvector(self.npvector * other.npvector)
            elif isinstance(other, KOrderMath.Quaternion):
                return other * self
            else:
                return self.from_npvector(self.npvector * other)
        
        def __rmul__(self, other):
            return self.__mul__(other)

        def __div__(self, scalar_value):
            if (type(scalar_value) is not float) and (type(scalar_value) is not long) and (type(scalar_value) is not int):
                raise ValueError("The Vector you are trying to divide by is not a float")

            divided_npvector = self.npvector
            divided_npvector[0] = divided_npvector[0] / scalar_value
            divided_npvector[1] = divided_npvector[1] / scalar_value
            divided_npvector[2] = divided_npvector[2] / scalar_value

            return self.from_npvector(divided_npvector)

        # Use mod operator to calculate the dot product between two vectors.
        # Eg. v1 % v2, gives the dot product of two vectors
        def __mod__(self, other):
            if not isinstance(other, KOrderMath.Vector):
                raise ValueError("You can only use dot between two KOrderMath.Vector s")

            return np.dot(self.npvector, other.npvector)

        # Use floor div operator to calculate the cross product between two vectors.
        # Eg. v1 // v2, gives the cross product of the two vectors.
        # Note v1 // v2 is not equal to v2 // v1
        def __floordiv__(self, other):
            if not isinstance(other, KOrderMath.Vector):
                raise ValueError("You can only use cross product between two KOrderMath.Vector s")

            return self.from_npvector(np.cross(self.npvector, other.npvector))

        # To string overload
        def __str__(self):
            return "x: " + "{:.3f}".format(self.x) + ", y: " + "{:.3f}".format(self.y) + ", z: " + "{:.3f}".format(self.z)

        def magnitude(self):
            length = nla.norm(self.npvector, axis=0)
            return length

        def normalize(self, raise_exception=False):
            length = nla.norm(self.npvector, axis=0)
            if np.isclose(length, 0.0):
                if raise_exception:
                    raise ValueError("The Vector you are trying to normalize has 0 length")
                return self
            return self.from_npvector(self.npvector / length)


    ###########################################################################################
    # QUTERNION respresents a point or a direction in 3D space.
    # Our co-ordinate system will follow the convention:
    # X Axis is forward
    # Y Axis is right
    # Z Axis is up
    ###########################################################################################
    
    class Quaternion:
        def normalize(self, raise_exception=False):
            length = nla.norm(self.npvector, axis=0)
            if np.isclose(length, 0.0):
                if raise_exception:
                    raise ValueError("The Vector you are trying to normalize has 0 length")
                return self
            return self.from_npvector(self.npvector / length)

        def get_axisangle(self):
            axis = KOrderMath.Vector.from_npvector(self.npvector[1:])
            axis = axis.normalize()

            angle = acos(self.w) * 2.0

            return angle, axis

        def __init__(self, w, x, y, z):
            self.npvector = np.array([w, x, y, z])
            self.w = self.npvector[0]
            self.x = self.npvector[1]
            self.y = self.npvector[2]
            self.z = self.npvector[3]
            [self.angle, self.axis] = self.get_axisangle()
            
        @classmethod
        def from_npvector(cls, npvector):
            return cls(npvector[0], npvector[1], npvector[2], npvector[3])

        @classmethod
        def from_axisangle(cls, axis, angle):
            if not isinstance(axis, KOrderMath.Vector):
                raise ValueError("Axis should be described as a KOrderMath.Vector")

            theta = angle
            axis = axis.normalize()

            return cls._axisangle_to_q(axis, theta)

        @classmethod
        def as_pure(cls, axis):
            if not isinstance(axis, KOrderMath.Vector):
                raise ValueError("Axis should be described as a KOrderMath.Vector")

            return KOrderMath.Quaternion(0.0, axis.x, axis.y, axis.z)

        @classmethod
        def _axisangle_to_q(cls, axis, angle):
            w = cos(angle/2.)
            x = axis.x * sin(angle/2.)
            y = axis.y * sin(angle/2.)
            z = axis.z * sin(angle/2.)

            return KOrderMath.Quaternion(w,x,y,z)

        # To string overload
        def __str__(self):
            return "angle: " + "{:.3f}".format(self.angle) + ", axis: " + str(self.axis)
        
        def print_quat(self):
            return "w: " + "{:.3f}".format(self.w) + "x: " + "{:.3f}".format(self.x) + ", y: " + "{:.3f}".format(self.y) + ", z: " + "{:.3f}".format(self.z)

        def __mul__(self, b):
            if isinstance(b, KOrderMath.Quaternion):
                return self._multiply_with_quaternion(b)
            elif isinstance(b, KOrderMath.Vector):
                return self._multiply_with_vector(b)
            else:
                raise ValueError("Multiplication with unknown type " + str(type(b)))

        def __rmul__(self, other):
            return self.__mul__(other)

        def get_conjugate(self):
            conjugate = KOrderMath.Quaternion(self.w, -self.x, -self.y, -self.z)
            return conjugate

        def _multiply_with_quaternion(self, q2):
            w1 = self.w
            x1 = self.x
            y1 = self.y
            z1 = self.z

            w2 = q2.w
            x2 = q2.x
            y2 = q2.y
            z2 = q2.z
            
            w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
            x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
            y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
            z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2

            result = KOrderMath.Quaternion(w, x, y, z)
            return result

        def _multiply_with_vector(self, v):
            q = self.normalize()
            q2 = KOrderMath.Quaternion.as_pure(v)
            rotated_quaternion = (q.get_conjugate() * q2 * q)
            return KOrderMath.Vector(rotated_quaternion.x, rotated_quaternion.y, rotated_quaternion.z)

    
"""
SPACE FOR TESTING ONLY

v = KOrderMath.Vector(10, 12, 0)
v2 = KOrderMath.Vector(11, 15, 0)



dot = v2 % v
v3 = v - v2
print v3.x
print dot

print v2.normalize()

print v * 2.0
print 2 * v
print v * v2
print v / 2.0
print v // v2

up = KOrderMath.Vector(0, 0, 1)

q = KOrderMath.Quaternion.from_axisangle(up, KOrderMath.convert_degrees_to_radians(45.0))

print q

qconj = q.get_conjugate()
print qconj

right = KOrderMath.Vector(0, 1, 0)
print "Before: " + str(right)
right = right * q
print "Rotated: " + str(right)

"""