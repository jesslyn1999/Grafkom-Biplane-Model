from OpenGL.GL import *
import math
from functools import reduce
import threading
import time
import numpy

class Vector:
    '''Constains the x, y and z information'''

    def __init__(self, x, y, z = 0):
        self.vector = (x, y, z)

    def set_x(self, val):
        self.vector = (val, self.vector[1], self.vector[2])

    def get_x(self):
        return self.vector[0]

    def set_y(self, val):
        self.vector = (self.vector[0], val, self.vector[2])

    def get_y(self):
        return self.vector[1]

    def set_z(self, val):
        self.vector = (self.vector[0], self.vector[1], val)

    def get_z(self):
        return self.vector[2]

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    def cross(self, other):
        return Vector(self.y*other.z-self.z*other.y, self.z*other.x-self.x*other.z, self.x*other.y-self.y*other.x)

    def normalized(self):
        '''Normalize the vector, length = 1
        Args:
            vector (Vector or list or tuple; if list or tuple, then len(vector) = 3): Vector to normalize.
        Returns:
            normalized vector.
        '''
        length = Vector.length(self)
        if isinstance(self, Vector):
            if length > 0:
                x, y, z = self.vector
                return Vector(x / length, y / length, z / length)
            else:
                return Vector(0, 0, 0)
        else:
            raise TypeError("unable to normalize type: {}".format(self.__class__.__name__))

    @staticmethod
    def Normalize(obj):
        '''Normalize the vector, length = 1
        Args:
            vector (Vector or list or tuple; if list or tuple, then len(vector) = 3): Vector to normalize.
        Returns:
            normalized vector.
        '''
        if isinstance(obj, Vector):
            x, y, z = obj.vector
        elif (isinstance(obj, tuple) or (isinstance(obj, list))) and len(obj) == 3:
            x, y, z = obj
        else:
            raise TypeError("unable to normalize type: {}".format(obj.__class__.__name__))
        length = Vector.LengthOf(obj)
        if isinstance(obj, Vector):
            return Vector(x / length, y / length, z / length)
        elif isinstance(obj, tuple):
            return (x / length, y / length, z / length)
        elif isinstance(obj, list):
            return [x / length, y / length, z / length]

    def length(self):
        '''Length of the vector
        Args:
            vector (Vector or list or tuple; if list or tuple, then len(vector) = 3): Vector to get the length of.
        Returns:
            float: length of the vector.
        '''
        if isinstance(self, Vector):
            x, y, z = self.vector
        else:
            raise TypeError("unable to get the vector length of type: {}".format(self.__class__.__name__))
        return (x**2 + y**2 + z**2)**0.5
    
    @staticmethod
    def LengthOf(obj):
        '''Length of an object
        Args:
            vector (Vector): Vector to get the length of.
        Overloads:
            tuple (list or tuple): Vector to get the length of.
        Returns:
            float: length of the vector.
        '''
        if isinstance(obj, Vector):
            x, y, z = obj.vector
        elif (isinstance(obj, tuple) or (isinstance(obj, list))) and len(obj) == 3:
            x, y, z = obj
        else:
            raise TypeError("unable to get the vector length of type: {}".format(obj.__class__.__name__))
        return (x**2 + y**2 + z**2)**0.5

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Vector(self.x + other, self.y + other, self.z + other)
        else:
            raise TypeError("unsupported operand '+' between: {} and {}".format(self.__class__.__name__, other.__class__.__name__))

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Vector(self.x - other, self.y - other, self.z - other)
        else:
            raise TypeError("unsupported operand '-' between: {} and {}".format(self.__class__.__name__, other.__class__.__name__))

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Vector(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError("unsupported operand '*' between: {} and {}".format(self.__class__.__name__, other.__class__.__name__))

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Vector(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError("unsupported operand '/' between: {} and {}".format(self.__class__.__name__, other.__class__.__name__))

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)

class Transform:

    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0)):
        self.position = position
        self.rotation = rotation
        self.matrix = TransformationMatrix()
        self.reset()
        self.parent = None
        self.childs = []
        self.owner = None

    def setParent(self, transform):
        if isinstance(transform, Transform):
            if self.parent:
                self.parent.childs.remove(self)
            self.parent = transform
            self.parent.childs.append(self)
        else:
            raise TypeError('unable')

    def addChild(self, transform):
        transform.setParent(self)

    def translate(self, x, y, z):
        self.position = (self.position[0] + x, self.position[1] + y, self.position[2] + z)
        self.reset()

    def rotate(self, x, y, z):
        self.rotation = (self.rotation[0] + x, self.rotation[1] + y, self.rotation[2] + z)
        self.reset()

    def apply(self):
        if self.parent:
            self.parent.apply()
        # self.matrix.apply()
        glTranslate(*self.position)
        glRotated(self.rotation[0], -1, 0, 0)
        glRotated(self.rotation[1], 0, -1, 0)
        glRotated(self.rotation[2], 0, 0, -1)

    def world_position(self):
        matrix = TransformationMatrix()
        # Get top level parent.
        parent = self.parent
        parents = []
        while parent:
            parents.append(parent)
            parent = parent.parent
        for p in reversed(parents):
            matrix *= p.matrix
        return Vector(*((matrix * self.position)[:-1]))

    def reset(self):
        # Set positional matrix.
        self.positional_matrix = TransformationMatrix.translate(*self.position)
        # Set rotational matrix.
        self.rotational_matrix = TransformationMatrix.from_euler_angles(*self.rotation)
        # Set the actual matrix of the camera.
        self.matrix.set_identity()
        self.matrix.multiply(self.positional_matrix)
        self.matrix.multiply(self.rotational_matrix)

class TransformationMatrix:

    def __init__(self, *values):
        if values:
            self.reset(*values)
        else:
            self.set_identity()

    def apply(self):
        glMultMatrixf(self.c_values())

    def c_values(self):
        return self.values

    def reset(self, *values):
        '''Accepts 16 float values'''
        if len(values) == 16:
            self.values = numpy.array(values, dtype=numpy.float32).reshape((4, 4))
            self.values_transposed = numpy.transpose(numpy.array(values, dtype=numpy.float32).reshape((4, 4)))
        else:
            raise ValueError("expected 16 float values, got " + len(values))

    def set_identity(self):
        self.reset(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        )

    def __str__(self):
        return '[' + reduce(lambda x, y: str(x) + ', ' + str(y), self.values) + ']'

    def multiply(self, other):
        if isinstance(other, TransformationMatrix):
            self.values = numpy.matmul(self.values, other.values)
            self.values_transposed = numpy.matmul(self.values_transposed, other.values_transposed)
        else:
            raise TypeError("unsupported multiplication between: '{}' and '{}'".format(self.__class__.__name__, other.__class__.__name__))

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            # Multiplication with scalar
            return TransformationMatrix(*[x * other for x in self.values])
        elif isinstance(other, tuple):
            # Multiplication with tuple.
            if len(other) < 4:
                other = (*other, *[1 for _ in range(0, 4 - len(other))])
            # result = (
            #     sum([self.values[i * 4] * other[i] for i in range(0, 4)]),
            #     sum([self.values[1 + i * 4] * other[i] for i in range(0, 4)]),
            #     sum([self.values[2 + i * 4] * other[i] for i in range(0, 4)]),
            #     sum([self.values[3 + i * 4] * other[i] for i in range(0, 4)]),
            # )
            # return result[:count]
            return numpy.matmul(self.values_transposed, other)
        elif isinstance(other, list):
            # Multiplication with list.
            if len(other) < 4:
                other = [*other, *[1 for _ in range(0, 4 - len(other))]]
            # result = [
            #     sum([self.values[i * 4] * other[i] for i in range(0, 4)]),
            #     sum([self.values[1 + i * 4] * other[i] for i in range(0, 4)]),
            #     sum([self.values[2 + i * 4] * other[i] for i in range(0, 4)]),
            #     sum([self.values[3 + i * 4] * other[i] for i in range(0, 4)]),
            # ]
            # return result[:count]
            return numpy.matmul(self.values_transposed, other)
        elif isinstance(other, numpy.ndarray):
            # Multiplication with ndarray.
            return numpy.matmul(self.values_transposed, other)
        elif isinstance(other, Vector):
            # Multiplication with Vector.
            point = (other.x, other.y, other.z, 1)
            result = self * point
            new = Vector(*result[:-1])
            return new
        elif isinstance(other, TransformationMatrix):
            # Multiplication with other matrix.
            result = TransformationMatrix()
            result.multiply(self)
            result.multiply(other)
            return result
        else:
            raise TypeError("unsupported operand type(s) for *: '{}' and '{}'".format(self.__class__.__name__, other.__class__.__name__))

    @staticmethod
    def translate(x, y, z):
        return TransformationMatrix(
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            x, y, z, 1.0
        )
    
    @staticmethod
    def dilate(k):
        return TransformationMatrix(
            k, 0.0, 0.0, 0.0,
            0.0, k, 0.0, 0.0,
            0.0, 0.0, k, 0.0,
            0.0, 0.0, 0.0, 1.0
        )

    @staticmethod
    def shear(src, dest, k):
        return TransformationMatrix(
            1 + (k * src[0] * dest[0]), (k * src[1] * dest[0]), (k * src[2] * dest[0]), 0.0,
            (k * src[0] * dest[1]), 1 + (k * src[1] * dest[1]), (k * src[2] * dest[1]), 0.0,
            (k * src[0] * dest[2]), (k * src[1] * dest[2]), 1 + (k * src[2] * dest[2]), 0.0,
            0.0, 0.0, 0.0, 1.0
        )

    @staticmethod
    def stretch(x, y, z):
        return TransformationMatrix(
            x, 0.0, 0.0, 0.0,
            0.0, y, 0.0, 0.0,
            0.0, 0.0, z, 0.0,
            0.0, 0.0, 0.0, 1.0
        )

    @staticmethod
    def from_euler_angles(x, y, z):
        matrix = TransformationMatrix()
        matrix.multiply(TransformationMatrix.rotate(-y, (0, 1, 0)))
        matrix.multiply(TransformationMatrix.rotate(-x, (1, 0, 0)))
        matrix.multiply(TransformationMatrix.rotate(-z, (0, 0, 1)))
        return matrix

    @staticmethod
    def reflect_point(x, y, z):
        retval = []
        point = (x, y, z)
        if point != (0, 0, 0):
            retval.append(TransformationMatrix.translate(-x, -y, -z))
        retval.append(TransformationMatrix(
            -1, 0, 0, 0,
            0, -1, 0, 0,
            0, 0, -1, 0,
            0, 0, 0, 1,
        ))
        if point != (0, 0, 0):
            retval.append(TransformationMatrix.translate(x, y, z))
        if len(retval) == 1:
            return retval[0]
        elif len(retval) > 1:
            # Multiply all the matrix and collapse them into a single matrix.
            collapsed = retval[0]
            for i in range(1, len(retval)):
                collapsed *= retval[i]
            return collapsed
        return retval

    @staticmethod
    def reflect_line(vector, point=(0, 0, 0)):
        if len(vector) != 3:
            raise ValueError("invalid vector: {}".format(vector))
        retval = []
        x, y, z = point
        if point != (0, 0, 0):
            retval.append(TransformationMatrix.translate(-x, -y, -z))
        retval.append(TransformationMatrix.rotate(180, vector))
        if point != (0, 0, 0):
            retval.append(TransformationMatrix.translate(x, y, z))
        if len(retval) == 1:
            return retval[0]
        elif len(retval) > 1:
            # Multiply all the matrix and collapse them into a single matrix.
            collapsed = retval[0]
            for i in range(1, len(retval)):
                collapsed *= retval[i]
            return collapsed
        return retval


    @staticmethod
    def rotate(angle, axis, point=None):
        if len(axis) != 3:
            raise ValueError("invalid axis: {}".format(axis))
        retval = []
        if point and point != (0, 0, 0):
            retval.append(TransformationMatrix.translate(*[-x for x in point]))
        if axis == (0, 0, 1) or axis == (0, 0, -1):
            _, _, z = axis
            if z == 1:
                angle = math.radians(angle)
            else:
                angle = math.radians(-angle)
            retval.append(TransformationMatrix(
                math.cos(angle), math.sin(angle), 0.0, 0.0,
                -math.sin(angle), math.cos(angle), 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0
            ))
        elif axis == (0, 1, 0) or axis == (0, -1, 0):
            _, y, _ = axis
            if y == 1:
                angle = math.radians(angle)
            else:
                angle = math.radians(-angle)
            retval.append(TransformationMatrix(
                math.cos(angle), 0.0, -math.sin(angle), 0.0,
                0.0, 1.0, 0.0, 0.0,
                math.sin(angle), 0.0, math.cos(angle), 0.0,
                0.0, 0.0, 0.0, 1.0
            ))
        elif axis == (1, 0, 0) or axis == (-1, 0, 0):
            x, _, _ = axis
            if x == 1:
                angle = math.radians(angle)
            else:
                angle = math.radians(-angle)
            retval.append(TransformationMatrix(
                1.0, 0.0, 0.0, 0.0,
                0.0, math.cos(angle), math.sin(angle), 0.0,
                0.0, -math.sin(angle), math.cos(angle), 0.0,
                0.0, 0.0, 0.0, 1.0
            ))
        else:
            x, y, z = axis
            # Align axis with xz plane.
            x_angle = math.degrees(math.atan2(y, z))
            level_xz = TransformationMatrix.rotate(x_angle, (1, 0, 0))
            # Align new axis with z axis.
            nx, ny, nz, _ = level_xz * (x, y, z, 1)
            y_angle = -math.degrees(math.atan2(nx, nz))
            level_z = TransformationMatrix.rotate(y_angle, (0, 1, 0))
            # Rotate around the z axis.
            rotation = TransformationMatrix.rotate(angle, (0, 0, 1))
            # Reverse alignment of z axis.
            i_level_z = TransformationMatrix.rotate(-y_angle, (0, 1, 0))
            # Reverse alignment of xz plane.
            i_level_xz = TransformationMatrix.rotate(-x_angle, (1, 0, 0))
            # Append individual transformation matrix to return value.
            retval.append(level_xz)
            retval.append(level_z)
            retval.append(rotation)
            retval.append(i_level_z)
            retval.append(i_level_xz)
        if point and point != (0, 0, 0):
            retval.append(TransformationMatrix.translate(*point))
        if len(retval) == 1:
            return retval[0]
        elif len(retval) > 1:
            # Multiply all the matrix and collapse them into a single matrix.
            collapsed = retval[0]
            for i in range(1, len(retval)):
                collapsed *= retval[i]
            return collapsed

class RotateOverTime(threading.Thread):

    def __init__(self, angle, axis, pivot, speed=360, callback=None):
        super().__init__()
        self.running = False
        self.current = TransformationMatrix()
        self.target = angle
        self.axis = axis
        self.pivot = pivot
        '''Duration is angle / speed.'''
        self.duration = abs(angle / speed)
        self.callback = callback

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        # identity = [
        #     1, 0, 0, 0,
        #     0, 1, 0, 0,
        #     0, 0, 1, 0,
        #     0, 0, 0, 1,
        # ]
        start_time = time.time()
        current_time = time.time()
        delay = 0.01
        while self.running and (current_time - start_time) < self.duration:
            current_angle = (current_time - start_time) / self.duration * self.target
            self.current.reset(*TransformationMatrix.rotate(current_angle, self.axis, self.pivot).values)
            current_time = time.time()
            time.sleep(delay)
        self.current.reset(*TransformationMatrix.rotate(self.target, self.axis, self.pivot).values)
        if self.callback:
            self.callback(self)

class TransformOverTime(threading.Thread):

    def __init__(self, target, duration=1, callback=None):
        super().__init__()
        self.running = False
        self.current = target
        self.target = target.values
        self.duration = duration
        self.callback = callback

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        identity = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ]
        start_time = time.time()
        current_time = time.time()
        delay = 0.01
        while self.running and (current_time - start_time) < self.duration:
            current = list(identity[i] + (self.target[i] - identity[i]) * (current_time - start_time) / self.duration for i in range(0, 16))
            self.current.reset(*current)
            current_time = time.time()
            time.sleep(delay)
        self.current.reset(*self.target)
        if self.callback:
            self.callback(self)
        