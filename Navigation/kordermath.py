import numpy as np
from numpy import linalg as nla

###########################################################################################
# KORDERMATH is the high level namespace for our Math Commons.
###########################################################################################
class KOrderMath:
    def convert_degrees_to_radians(self, degrees):
        return np.deg2rad(degrees)

    def convert_radians_to_degrees(self, degrees):
        return np.rad2deg(degrees)

    def get_projection(self, of_vector, on_vector):
        on_vector_mag = on_vector.magnitude()
        on_vector_norm = on_vector / on_vector_mag
        projection_comp = (of_vector % on_vector) / (on_vector_mag)
        projection = projection_comp * on_vector_norm
        return projection

    

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
            return self.from_npvector(self.npvector + other.npvector)

        def __sub__(self, other):
            return self.from_npvector(self.npvector - other.npvector)
        
        def __mul__(self, other):
            if type(other) is type(self):
                return self.from_npvector(self.npvector * other.npvector)
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
            return np.dot(self.npvector, other.npvector)

        # Use floor div operator to calculate the cross product between two vectors.
        # Eg. v1 // v2, gives the cross product of the two vectors.
        # Note v1 // v2 is not equal to v2 // v1
        def __floordiv__(self, other):
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
"""