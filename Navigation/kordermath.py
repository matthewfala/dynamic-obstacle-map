import numpy as np
from numpy import linalg as nla
from math import sin, cos, acos, sqrt

##################################################################################################################
# kordermath is the high level namespace for our Math Commons.
# @Guidelines:
# *** When creating a new function please attach @Brief, @Author, @Param and @Return to describe the function in
#     comments above the function, if the function is meant to be used as an utilitiy function. 
#     Look get_projection for example.
# *** When attaching the author name, please add the email as well for easy contact access.
#     Eg @Author: Kishore Venkateshan (kishorev@usc.edu)
# *** For all class functions under kordermath that haven't been tagged with an author,
#     assume the author of the function to be the author specified in the class.
# *** Classes can be created with just an @Brief and an @Author tag. Please provide a brief structure of the 
#     class if possible. For example look at the Vector Class
##################################################################################################################
class kordermath:
    # @Brief: Clamps a value between min and max values
    #         Supported Types: (float, int)
    # @Author: Kishore Venkateshan (kishorev@usc.edu)
    # @Param: value_to_clamp  - The value to be clamped
    # @Param: min_value - The minimum value of the value to be clamped
    # @Param: max_value - The maximum value of the value to be clamped
    # @Return: The new value clamped between min and max values
    @classmethod
    def clamp(cls, value_to_clamp, min_value, max_value):
        if type(value_to_clamp) is not type(min_value) or type(value_to_clamp) is not type(max_value):
            raise ValueError("Can't clamp value with min and max values of different type")    

        if type(value_to_clamp) is float or type(value_to_clamp) is int:
            return max(min(value_to_clamp, max_value), min_value)
        
        raise ValueError("Type of value is not supported")

    
    # @Brief: Gets the projection vector of a vector on another vector
    # @Author: Kishore Venkateshan (kishorev@usc.edu)
    # @Param: of_vector (kordermath.vector) - The vector to be projected
    # @Param: on_vector (kordermath.vector) - The vector on which of_vector will be projected
    # @Return: (kordermath.vector) - Projected vector that will be in the direction of on_vector
    @classmethod
    def get_projection(cls, of_vector, on_vector):
        if not isinstance(of_vector, kordermath.vector) or not isinstance(on_vector, kordermath.vector):
            raise ValueError("You can only get projection of one kordermath.vector on another kordermath.vector")

        on_vector_mag = on_vector.magnitude()
        on_vector_norm = on_vector / on_vector_mag
        projection_comp = (of_vector % on_vector) / (on_vector_mag)
        projection = projection_comp * on_vector_norm
        return projection


    # @Brief: Rotates a given vector on the 2D plane by the specified angle which will be considered as
    #         positive for counter clockwise rotation  
    # @Author: Kishore Venkateshan (kishorev@usc.edu)
    # @Param: vector (kordermath.vector) - The vector to be rotated
    # @Param: angle (double) - The rotation angle in radians 
    # @Return: (kordermath.vector) - Rotated vector
    @classmethod
    def rotate_vector_2D(cls, vector, angle):
        rotation_quat = kordermath.quaternion.from_axisangle(kordermath.vector.up(), angle)
        return vector * rotation_quat


    # @Brief: Gives the angle of rotation between two vectors in radians
    # @Author: Kishore Venkateshan (kishorev@usc.edu)
    # @Param: v1 (kordermath.vector)
    # @Param: v2 (kordermath.vector)
    # @Return: (double) - angle between in the vectors in radians
    @classmethod
    def angle_between_vectors(cls, v1, v2):
        v1norm = v1.normalize()
        v2norm = v2.normalize()

        dot = float(v1norm % v2norm)
        dot = kordermath.clamp(dot, -1.0, 1.0)

        angle = acos(dot)
        return angle


    ###########################################################################################
    # @Brief:
    # 'angle' respresents the arc length subtended between two unit vectors.
    # Why angle instead of float?
    # --- Using float decouples degrees and radians. You could potentially end up passing in 
    #     a degree to a function that was expecting radians. Or you could convert to degrees
    #     and forget to change it back to radians which will end up using incorrect values.
    # --- An angle class could encapsulate a bunch of other angle related math such as wrapping
    #     angles, normalizing from -pi to pi and so on.
    # @Author: Kishore Venkateshan (kishorev@usc.edu)
    ###########################################################################################
    class angle(object):
        # @Brief: Convert from angle in degrees to radians
        # @Author: Kishore Venkateshan (kishorev@usc.edu)
        # @Param: degrees  - The angle in degrees
        # @Return: The new angle measured in radians
        @classmethod
        def convert_degrees_to_radians(cls, degrees):
            return np.deg2rad(degrees)


        # @Brief: Convert from angle in radians to degrees
        # @Author: Kishore Venkateshan (kishorev@usc.edu)
        # @Param: radians  - The angle in degrees
        # @Return: The new angle measured in degrees
        @classmethod
        def convert_radians_to_degrees(cls, radians):
            return np.rad2deg(radians)


        @classmethod
        def from_degrees(cls, degrees):
            return kordermath.angle(cls.convert_degrees_to_radians(degrees))


        # @Brief: Gives the angle of rotation between two vectors in degress
        # @Author: Kishore Venkateshan (kishorev@usc.edu)
        # @Param: v1 (kordermath.vector)
        # @Param: v2 (kordermath.vector)
        # @Return: (double) - angle between in the vectors in degrees
        @classmethod
        def angle_between_vectors_in_degrees(cls, v1, v2):
            return cls.convert_radians_to_degrees(kordermath.angle_between_vectors(v1, v2))


        def __init__(self, radians):
            self._radians = radians
            self._degrees = self.convert_radians_to_degrees(self._radians)

        def __str__(self):
            return "{:.2f}".format(self.degrees) + " deg"

        @property
        def radians(self):
            return self._radians
        @radians.setter
        def radians(self, value):
            self._radians = value
            self._degrees = self.convert_radians_to_degrees(self._radians)

        @property
        def degrees(self):
            return self._degrees
        @degrees.setter
        def degrees(self, value):
            self._degrees = value
            self._radians = self.convert_degrees_to_radians(self._degrees)


    ###########################################################################################
    # @Brief:
    # 'vector' respresents a point or a direction in 3D space.
    # Our co-ordinate system will follow the convention:
    # Y Axis is forward
    # X Axis is right
    # Z Axis is up
    # which is the right handed co-ordinate system
    # @Author: Kishore Venkateshan (kishorev@usc.edu)
    ###########################################################################################
    class vector(object):
        @classmethod
        def zero(cls):
            return kordermath.vector(0.0, 0.0, 0.0)

        @classmethod
        def up(cls):
            return kordermath.vector(0.0, 0.0, 1.0)

        @classmethod
        def right(cls):
            return kordermath.vector(1.0, 0.0, 0.0)

        @classmethod
        def forward(cls):
            return kordermath.vector(0.0, 1.0, 0.0)

        def __init__(self, x, y, z):
            self.__npvector = np.array([x, y, z])
            self.__x = self.__npvector[0]
            self.__y = self.__npvector[1]
            self.__z = self.__npvector[2]


        ######################################################################################
        # vector properties
        ######################################################################################
        @property
        def x(self):
            return self.__x
        @x.setter
        def x(self, value):
            self.__x = value
            self.__npvector[0] = self.__x

        @property
        def y(self):
            return self.__y
        @y.setter
        def y(self, value):
            self.__y = value
            self.__npvector[1] = self.__y

        @property
        def z(self):
            return self.__z
        @z.setter
        def z(self, value):
            self.__z = value
            self.__npvector[2] = self.__z

        @property
        def npvector(self):
            self.__npvector = np.array([self.__x, self.__y, self.__z])
            return self.__npvector



        @classmethod
        def from_npvector(cls, npvector):
            return cls(npvector[0], npvector[1], npvector[2])

        def __add__(self, other):
            if not isinstance(other, kordermath.vector):
                raise ValueError("You can only add a kordermath.vector to another kordermath.vector")

            return self.from_npvector(self.npvector + other.npvector)

        def __sub__(self, other):
            if not isinstance(other, kordermath.vector):
                raise ValueError("You can only subtract a kordermath.vector to another kordermath.vector")

            return self.from_npvector(self.npvector - other.npvector)
        
        def __mul__(self, other):
            if isinstance(other, kordermath.vector):
                return self.from_npvector(self.npvector * other.npvector)
            elif isinstance(other, kordermath.quaternion):
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
            if not isinstance(other, kordermath.vector):
                raise ValueError("You can only use dot between two kordermath.vector s")

            return np.dot(self.npvector, other.npvector)

        # Use floor div operator to calculate the cross product between two vectors.
        # Eg. v1 // v2, gives the cross product of the two vectors.
        # Note v1 // v2 is not equal to v2 // v1
        def __floordiv__(self, other):
            if not isinstance(other, kordermath.vector):
                raise ValueError("You can only use cross product between two kordermath.vector s")

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


    ################################################################################################################
    # @Brief:
    # 'quaternion' is used to represent rotations in 3D Math.
    # The easiest way to visualize quaternion is through an axis and an angle.
    # from_axisangle and get_axisangle will be primarily used to create / visualize quaternions
    # To rotate a vector 'v' (kordermath.vector) about an axis 'a' (also a kordermath.vector) by angle 'r' (double)
    # do v * kordermath.quaternion.from_axisangle(a, r)
    # @Author: Kishore Venkateshan (kishorev@usc.edu)
    ################################################################################################################ 
    class quaternion(object):
        def normalize(self, raise_exception=False):
            length = nla.norm(self.npvector, axis=0)
            if np.isclose(length, 0.0):
                if raise_exception:
                    raise ValueError("The Vector you are trying to normalize has 0 length")
                return self
            return self.from_npvector(self.npvector / length)

        def get_axisangle(self):
            axis = kordermath.vector.from_npvector(self.npvector[1:])
            axis = axis.normalize()

            angle = acos(self.w) * 2.0

            return angle, axis

        def __init__(self, w, x, y, z):
            self.__npvector = np.array([w, x, y, z])
            self.__w = self.__npvector[0]
            self.__x = self.__npvector[1]
            self.__y = self.__npvector[2]
            self.__z = self.__npvector[3]
            [self.__angle, self.__axis] = self.get_axisangle()


        ######################################################################################
        # quaternion properties
        ######################################################################################
        @property
        def w(self):
            return self.__w

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        @property
        def z(self):
            return self.__z
        
        @property
        def npvector(self):
            self.__npvector = np.array([self.__w, self.__x, self.__y, self.__z])
            return self.__npvector

        @property
        def angle(self):
            return self.__angle

        @property
        def axis(self):
            return self.__axis

            
        @classmethod
        def from_npvector(cls, npvector):
            return cls(npvector[0], npvector[1], npvector[2], npvector[3])

        @classmethod
        def from_axisangle(cls, axis, angle):
            if not isinstance(axis, kordermath.vector):
                raise ValueError("Axis should be described as a kordermath.vector")

            theta = angle
            axis = axis.normalize()

            return cls._axisangle_to_q(axis, theta)

        @classmethod
        def __as_pure(cls, axis):
            if not isinstance(axis, kordermath.vector):
                raise ValueError("Axis should be described as a kordermath.vector")

            return kordermath.quaternion(0.0, axis.x, axis.y, axis.z)

        @classmethod
        def _axisangle_to_q(cls, axis, angle):
            w = cos(angle/2.)
            x = axis.x * sin(angle/2.)
            y = axis.y * sin(angle/2.)
            z = axis.z * sin(angle/2.)

            return kordermath.quaternion(w,x,y,z)

        # To string overload
        def __str__(self):
            return "angle: " + "{:.3f}".format(self.angle) + ", axis: " + str(self.axis)
        
        def print_quat(self):
            return "w: " + "{:.3f}".format(self.w) + "x: " + "{:.3f}".format(self.x) + ", y: " + "{:.3f}".format(self.y) + ", z: " + "{:.3f}".format(self.z)

        def __mul__(self, b):
            if isinstance(b, kordermath.quaternion):
                return self._multiply_with_quaternion(b)
            elif isinstance(b, kordermath.vector):
                return self._multiply_with_vector(b)
            else:
                raise ValueError("Multiplication with unknown type " + str(type(b)))

        def __rmul__(self, other):
            return self.__mul__(other)

        def get_conjugate(self):
            conjugate = kordermath.quaternion(self.w, -self.x, -self.y, -self.z)
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

            result = kordermath.quaternion(w, x, y, z)
            return result

        def _multiply_with_vector(self, v):
            q = self.normalize()
            q2 = kordermath.quaternion.__as_pure(v)
            rotated_quaternion = (q.get_conjugate() * q2 * q)
            return kordermath.vector(rotated_quaternion.x, rotated_quaternion.y, rotated_quaternion.z)

"""
SPACE FOR TESTING ONLY

v = kordermath.vector(10, 12, 0)
v2 = kordermath.vector(11, 15, 0)



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

up = kordermath.vector(0, 0, 1)

q = kordermath.quaternion.from_axisangle(up, kordermath.angle.convert_degrees_to_radians(45.0))

print q

qconj = q.get_conjugate()
print qconj

right = kordermath.vector(0, 1, 0)
print "Before: " + str(right)
right = right * q
print "Rotated: " + str(right)

#Tests for rotation. Ensure angle between vectors is correct. And ensure the magnitude is retained after rotation
#START
v = kordermath.vector(2, 3, 0)

r = kordermath.rotate_vector_2D(v, 0.3)

print v
print v.magnitude()
print r
print r.magnitude()

print kordermath.angle_between_vectors(v, r)
#END

"""