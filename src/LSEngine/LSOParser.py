import os, sys
import numpy
from .ShapeBuilder import MakeRenderObject, ConvertToTriangles, CollapseToTriangles
from OpenGL.GL import GL_TRIANGLES
from .Primitives  import TransformationMatrix
from .Mesh import Mesh

class LSOError(ValueError):
    pass

def SaveAsLSO(filename, verticesList, indicesList): # does not support texture yet
    vertices, indices = CollapseToTriangles(verticesList, indicesList)
    lines = []
    i = 0
    while i < len(vertices):
        lines.append("v {} {} {}\n".format(vertices[i], vertices[i + 1], vertices[i + 2]))
        i += 3
    i = 0
    while i < len(indices):
        if (indices[i] != indices[i + 1]) and (indices[i] != indices[i + 2]) and (indices[i + 1] != indices[i + 2]):
            lines.append("f {} {} {}\n".format(indices[i] + 1, indices[i + 1] + 1, indices[i + 2] + 1))
        i += 3

    with open(filename, 'w') as file:
        file.writelines(lines)

def ParseLSO(filename):
    '''
    Arguments:
        filename (string) : absolute path of the input file
    Returns:
        vertices (list): list of vertices
        indices (list): list of indices
    '''
    vertices = []
    texVertices = []
    indices = []
    texIndices = []
    line_idx = 0

    if os.path.splitext(filename)[1] == '.lso':
        with open(filename, 'r') as file:
            for line in file:
                line_idx += 1
                line = line.strip()
                if line:
                    if line[0] == '#': # Ignore comments
                        continue
                    data = line.split()
                    # add data to vertices
                    if data[0] == 'v':
                        for i in range(1, len(data)):
                            try:
                                vertices.append(float(data[i]))
                            except ValueError as e:
                                raise LSOError("unknown float value '{}' at line {}".format(data[i], line_idx)) from e
                    if data[0] == 'vt':
                        for i in range(1, len(data)):
                            try:
                                texVertices.append(float(data[i]))
                            except ValueError as e:
                                raise LSOError("unknown float value '{}' at line {}".format(data[i], line_idx)) from e
                    # add data to indices
                    elif data[0] == 'f':
                        for i in range(1, len(data)):
                            try:
                                split = data[i].split('/')
                                if len(split) == 1:
                                    indices.append(int(split[0]) - 1)
                                    texIndices.append(-1)
                                elif len(split) == 2:
                                    indices.append(int(split[0]) - 1)
                                    texIndices.append(int(split[1]) - 1)
                            except ValueError as e:
                                raise LSOError("unknown int value '{}' at line {}".format(data[i], line_idx)) from e

    return vertices, indices, texVertices, texIndices

def LoadLSO(filename):
    vertices, indices, texVertices, texIndices = ParseLSO(filename)
    return Mesh([(vertices, 3)], [(indices, GL_TRIANGLES, 0)], [texVertices], [(0, texIndices, 0)])

def GenerateFromLSO(filename):
    return MakeRenderObject(LoadLSO(filename))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        lines = []
        with open(sys.argv[1], 'r') as file:
            lines = file.readlines()
        if sys.argv[2] == 'translate':
            dx, dy, dz = [float(d) for d in sys.argv[3:]]
            i = 0
            for i in range(0, len(lines)):
                line = lines[i].strip()
                if line:
                    data = line.split()
                    if data[0] == 'v':
                        x, y, z = [float(d) for d in data[1:]]
                        lines[i] = 'v {} {} {}\n'.format(x + dx, y + dy, z + dz)
        elif sys.argv[2] == 'rotate':
            dx, dy, dz = [float(d) for d in sys.argv[3:]]
            mat = TransformationMatrix.from_euler_angles(dx, dy, dz)
            i = 0
            for i in range(0, len(lines)):
                line = lines[i].strip()
                if line:
                    data = line.split()
                    if data[0] == 'v':
                        vec = [float(d) for d in data[1:]]
                        vec = mat * vec
                        lines[i] = 'v {} {} {}\n'.format(*vec)
        with open(sys.argv[1], 'w') as file:
            file.writelines(lines)

