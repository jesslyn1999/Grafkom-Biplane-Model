from OpenGL.GL import GL_TRIANGLES, GL_TRIANGLE_STRIP
import math
from .Mesh import Mesh, MeshRenderer, ImmediateMeshRenderer
from . import Behaviour

def CollapseToTriangles(verticesList, indicesList):
    offset = []
    c_offset = 0
    vertices = []
    indices = []
    for vert, _ in verticesList:
        offset.append(c_offset)
        vertices.extend(vert)
        c_offset += len(vert)
    
    for ind, mode, VBO_id in indicesList:
        ind = ConvertToTriangles(ind, mode)
        off = offset[VBO_id]
        for i in ind:
            indices.append(i + off)
    return vertices, indices

def ConvertToTriangles(indices, currentMode):
    newIndices = []
    if currentMode == GL_TRIANGLE_STRIP:
        for i in range(0, len(indices) - 2):
            vert = []
            if i % 2 == 0:
                vert.append(indices[i])
                vert.append(indices[i + 1])
                vert.append(indices[i + 2])
            else:
                vert.append(indices[i + 1])
                vert.append(indices[i])
                vert.append(indices[i + 2])
            dup = (vert[0] == vert[1]) or (vert[1] == vert[2]) or (vert[0] == vert[2])
            if not dup:
                newIndices.extend(vert)
    else:
        newIndices = indices
    return newIndices

def MakeRenderObject(mesh):
    '''Create a render object by passing the information.
    Args:
        mesh (mesh): Mesh to make a render object out of.
    '''
    obj = Behaviour.LSObject()
    obj.add_component(MeshRenderer(mesh))
    return obj

def MakeImmediateRenderObject(mesh):
    '''Create a render object by passing the information.
    Args:
        mesh (mesh): Mesh to make a render object out of.
    '''
    obj = Behaviour.LSObject()
    obj.add_component(ImmediateMeshRenderer(mesh))
    return obj

def GenerateRenderObject(generatorFunc, *args):
    obj = Behaviour.LSObject()
    obj.add_component(MeshRenderer(generatorFunc(*args)))
    return obj

def GenerateImmediateRenderObject(generatorFunc, *args):
    obj = Behaviour.LSObject()
    mesh = generatorFunc(*args)
    for i in range(0, len(mesh.texIndicesList)):
        if (mesh.texIndicesList[i]):
            indices, v_id = mesh.texIndicesList[i]
            _, mode, _ = mesh.indicesList[i]
            indices = ConvertToTriangles(indices, mode)
            mesh.texIndicesList[i] = (i, indices, v_id)
    mesh = Mesh(mesh.verticesList, mesh.indicesList, mesh.texVerticesList, mesh.texIndicesList)
    obj.add_component(ImmediateMeshRenderer(mesh))
    for i in range(0, len(mesh.indicesList)):
        indices, mode, vbo_id = mesh.indicesList[i]
        indices = ConvertToTriangles(indices, mode)
        mesh.indicesList[i] = (indices, GL_TRIANGLES, vbo_id)
    return obj

def GenerateBlock(width, height, length):
    vertices = [
        -width/2, -height/2, -length/2,
        -width/2, -height/2, length/2,
        -width/2, height/2, length/2,
        -width/2, height/2, -length/2, 
        width/2, -height/2, -length/2,
        width/2, -height/2, length/2,
        width/2, height/2, length/2,
        width/2, height/2, -length/2,
        0, -height/2, 0,
        0, height/2, 0,
        -width/2, 0, 0,
        width/2, 0, 0,
        0, 0, -length/2,
        0, 0, length/2,
    ]
    normals = {
        
    }
    indices = [
        0, 1, 10,
        1, 2, 10,
        2, 3, 10,
        3, 0, 10,
        5, 4, 11,
        6, 5, 11,
        7, 6, 11,
        4, 7, 11,
        1, 0, 8,
        5, 1, 8,
        4, 5, 8,
        0, 4, 8,
        0, 3, 12,
        4, 0, 12,
        7, 4, 12,
        3, 7, 12,
        3, 2, 9,
        7, 3, 9,
        6, 7, 9,
        2, 6, 9,
        2, 1, 13,
        6, 2, 13,
        5, 6, 13,
        1, 5, 13,
    ]
    texVertices = [
        0, 0,
        1, 0,
        1, 1,
        0, 1,
        0.5, 0.5,
    ]
    texIndices = [
        3, 2, 4,
        2, 1, 4,
        1, 0, 4,
        0, 3, 4,
        3, 2, 4,
        2, 1, 4,
        1, 0, 4,
        0, 3, 4,
        3, 2, 4,
        2, 1, 4,
        1, 0, 4,
        0, 3, 4,
        3, 2, 4,
        2, 1, 4,
        1, 0, 4,
        0, 3, 4,
        3, 2, 4,
        2, 1, 4,
        1, 0, 4,
        0, 3, 4,
        3, 2, 4,
        2, 1, 4,
        1, 0, 4,
        0, 3, 4,
    ]
    verticesList = []
    verticesList.append((vertices, 3))
    indicesList = []
    indicesList.append((indices, GL_TRIANGLES, 0))
    texVerticesList = []
    texVerticesList.append(texVertices)
    texIndicesList = []
    texIndicesList.append((0, texIndices, 0))
    return Mesh(verticesList, indicesList, texVerticesList, texIndicesList)

def GenerateCylinder(radius, height, segments = 18):
    # Generate all vertices.
    vertices = [
        0, -height / 2, 0,
        0, height / 2, 0,
    ]
    texVertices = [
        0.25, 0.25,
        0.75, 0.25,
    ]
    for i in range(0, segments):
        texVertices.append(0.25 + (math.cos(-math.pi * 2 / segments * i) * 0.25))
        texVertices.append(0.25 + (math.sin(-math.pi * 2 / segments * i) * 0.25))
        vertices.append(math.cos(math.pi * 2 / segments * i) * radius)
        vertices.append(-height / 2)
        vertices.append(math.sin(math.pi * 2 / segments * i) * radius)
    for i in range(0, segments):
        texVertices.append(0.75 + (math.cos(math.pi * 2 / segments * i) * 0.25))
        texVertices.append(0.25 + (math.sin(math.pi * 2 / segments * i) * 0.25))
        vertices.append(math.cos(math.pi * 2 / segments * i) * radius)
        vertices.append(height / 2)
        vertices.append(math.sin(math.pi * 2 / segments * i) * radius)
    for i in range(0, segments):
        texVertices.append(1.0 / segments * i)
        texVertices.append(1.0)
    for i in range(0, segments):
        texVertices.append(1.0 / segments * i)
        texVertices.append(0.5)
    texVertices.append(1.0)
    texVertices.append(1.0)
    texVertices.append(1.0)
    texVertices.append(0.5)
    # Generate the indices for bottom segment.
    texIndicesBottom = []
    indicesBottom = []
    for i in range(2, segments + 2):
        indicesBottom.append(0)
        texIndicesBottom.append(0)
        indicesBottom.append(i)
        texIndicesBottom.append(i)
    indicesBottom.append(2)
    texIndicesBottom.append(2)
    # Generate the indices for middle segment.
    texIndicesMiddle = []
    indicesMiddle = []
    for i in range(2, segments + 2):
        indicesMiddle.append(i)
        texIndicesMiddle.append(2 * segments + i)
        indicesMiddle.append(i + segments)
        texIndicesMiddle.append(3 * segments + i)
    indicesMiddle.append(2)
    texIndicesMiddle.append(2 + segments * 4)
    indicesMiddle.append(2 + segments)
    texIndicesMiddle.append(3 + segments * 4)
    # Generate the indices for top segment.
    texIndicesTop = []
    indicesTop = []
    for i in range(2, segments + 2):
        indicesTop.append(i + segments)
        texIndicesTop.append(i + segments)
        indicesTop.append(1)
        texIndicesTop.append(1)
    indicesTop.append(2 + segments)
    texIndicesTop.append(2 + segments)
    
    verticesList = []
    verticesList.append((vertices, 3))
    indicesList = []
    indicesList.append((indicesBottom, GL_TRIANGLE_STRIP, 0))
    indicesList.append((indicesMiddle, GL_TRIANGLE_STRIP, 0))
    indicesList.append((indicesTop, GL_TRIANGLE_STRIP, 0))
    texVerticesList = []
    texVerticesList.append(texVertices)
    texIndicesList = []
    texIndicesList.append((0, texIndicesBottom, 0))
    texIndicesList.append((1, texIndicesMiddle, 0))
    texIndicesList.append((2, texIndicesTop, 0))

    return Mesh(verticesList, indicesList, texVerticesList, texIndicesList)