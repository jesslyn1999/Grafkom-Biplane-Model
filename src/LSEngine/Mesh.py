from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy
from .Behaviour import Component
from .Primitives import TransformationMatrix, Vector
from PIL import Image

solidcolor_vertex = """
    #version 120
    attribute vec3 position;
    uniform mat4 transform;
    void main()
    {
        gl_Position = transform * gl_ModelViewProjectionMatrix * vec4(position, 1.0f);
    }
    """

solidcolor_fragment = """
    # version 120
    uniform vec4 color;
    void main()
    {
        gl_FragColor = color;
    }
    """

class Mesh:

    def __init__(self, verticesList, indicesList, texVerticesList = [], texIndicesList = [], normalList = []):
        self.verticesList = verticesList
        self.indicesList = indicesList
        self.texVerticesList = texVerticesList
        s = 0
        if texIndicesList:
            s = max(texIndicesList, key=lambda x: x[0])[0] + 1
        self.texIndicesList = [None for _ in range(0, s)]
        for i, t, v_id in texIndicesList:
            self.texIndicesList[i] = (t, v_id)
        self.normalList = []
        if normalList:
            self.normalList = normalList
        else:
            for i in range(0, len(indicesList)):
                element, mode, VBO_id = self.indicesList[i]
                normals = []
                vertices, size = self.verticesList[VBO_id] 
                if mode == GL_TRIANGLES:
                    i = 0
                    verts = []
                    while i < len(element):
                        vert = []
                        for j in range(0, size):
                            vert.append(vertices[element[i] * 3 + j])
                        verts.append(vert)
                        if len(verts) == 3:
                            d1 = Vector(*[x for x in verts[1]]) - Vector(*[x for x in verts[0]])
                            d2 = Vector(*[x for x in verts[2]]) - Vector(*[x for x in verts[0]])
                            res = d1.cross(d2).normalized()
                            if res.x == 0:
                                res.x = 0
                            if res.y == 0:
                                res.y = 0
                            if res.z == 0:
                                res.z = 0
                            normals.append(res.x)
                            normals.append(res.y)
                            normals.append(res.z)
                            verts.clear()
                        i += 1
                elif mode == GL_TRIANGLE_STRIP:
                    # for i in range(0, len(element) - 2):
                    #     vert1 = None
                    #     vert2 = None
                    #     vert3 = None
                    #     if i % 2 == 1:
                    #         vert1 = vertices[element[i]]
                    #         vert2 = vertices[element[i + 1]]
                    #         vert3 = element[i + 2]
                    #     else:
                    #         vert1 = element[i + 1]
                    #         vert2 = element[i]
                    #         vert3 = element[i + 2]
                    #     d1 = vert2 - vert1
                    #     d2 = vert3 - vert1
                    pass
                # print(normals)
                self.normalList.append(normals)

class Texture:

    def __init__(self, filename):
        image = Image.open(filename)
        self.size_x = image.size[0]
        self.size_y = image.size[1]
        data = numpy.array(list(image.getdata()), dtype=numpy.int32)
        self.tex_id = glGenTextures(1)
        self.filename = filename

        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.size_x, self.size_y, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glBindTexture(GL_TEXTURE_2D, 0)

    def use(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)

    def unuse(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

    def __enter__(self):
        self.use()

    def __exit__(self, exc_type, exc_val, traceback):
        self.unuse()

class Material:

    def __init__(self, amb, diff, spec, emi, shine):
        self.ambient = amb
        self.diffuse = diff
        self.specular = spec
        self.emission = emi
        self.shininess = shine

    def use(self):
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular)
        glMaterialfv(GL_FRONT, GL_EMISSION, self.emission)
        glMaterialf(GL_FRONT, GL_SHININESS, self.shininess)

    def unuse(self):
        glMaterialfv(GL_FRONT, GL_AMBIENT, 0)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, 0)
        glMaterialfv(GL_FRONT, GL_SPECULAR, 0)
        glMaterialfv(GL_FRONT, GL_EMISSION, 0)
        glMaterialf(GL_FRONT, GL_SHININESS, 0)

class ImmediateMeshRenderer(Component):

    def __init__(self, clone=None):
        self.mesh = None
        self.tint_color = (1, 1, 1, 1)
        self.texture = None
        self.material = None
        
        if isinstance(clone, Mesh):
            self.mesh = clone
        elif isinstance(clone, ImmediateMeshRenderer):
            self.mesh = clone.mesh
            self.tint_color = clone.tint_color
            if clone.texture:
                # self.texture = Texture(clone.texture.filename)
                self.texture = clone.texture
            if clone.material:
                # self.material = Material(clone.material.ambient, clone.material.diffuse, clone.material.specular)
                self.material = clone.material

    def clone(self):
        return ImmediateMeshRenderer(self)

    def render(self):
        if self.mesh:
            if self.material:
                self.material.use()
            glColor(*self.tint_color)
            if self.texture:
                self.texture.use()
                for i in range(len(self.mesh.indicesList)):
                    element, mode, VBO_id = self.mesh.indicesList[i]
                    tex_coord = None
                    tex_vert = None
                    if i < len(self.mesh.texIndicesList):
                        if self.mesh.texIndicesList[i]:
                            tex_coord, vert_id = self.mesh.texIndicesList[i]
                            if vert_id < len(self.mesh.texVerticesList):
                                tex_vert = self.mesh.texVerticesList[vert_id]
                    glBegin(mode)
                    vertices, size = self.mesh.verticesList[VBO_id]
                    normals = self.mesh.normalList[i]
                    # for index in element:
                    for j in range(0, len(element)):
                        index = element[j]
                        if j % 3 == 0:
                            k = j // 3
                            if k < len(normals):
                                l = k * 3
                                glNormal(normals[l], normals[l + 1], normals[l + 2])
                        if tex_coord and tex_vert and j < len(tex_coord):
                            ind = tex_coord[j]
                            if ind >= 0:
                                glTexCoord(tex_vert[ind * 2], tex_vert[ind * 2 + 1])
                        vertex = []
                        for k in range(0, size):
                            vertex.append(vertices[(index * size) + k])
                        glVertex(*vertex)
                    glEnd()
                self.texture.unuse()
            else:
                for element, mode, VBO_id in self.mesh.indicesList:
                    glBegin(mode)
                    vertices, size = self.mesh.verticesList[VBO_id]
                    for index in element:
                        vertex = []
                        for i in range(0, size):
                            vertex.append(vertices[(index * size) + i])
                        glVertex(*vertex)
                    glEnd()
            if self.material:
                self.material.unuse()

class MeshRenderer(Component):

    def __init__(self, clone=None):
        self.VBOs = []
        self.EBOs = []
        self.shader = None
        self.tint_color = (1, 1, 1, 1)

        if isinstance(clone, Mesh):
            for vertices, size in clone.verticesList:
                self.GenerateVBO(vertices, size)
            for indices, mode, VBO_id in clone.indicesList:
                self.GenerateEBO(indices, mode, self.VBOs[VBO_id][0])
        elif isinstance(clone, MeshRenderer):
            self.VBOs = list(clone.VBOs)
            self.EBOs = list(clone.EBOs)
            self.shader = clone.shader
            self.tint_color = clone.tint_color

    def clone(self):
        return MeshRenderer(self)

    def GenerateVBO(self, vertices, size=3):
        '''
        Args:
            vertices (list) : List of vertices to be added in VBO.

        Returns:
            Buffers id.
        '''
        # cast vertices to numpy array
        vertices = numpy.array(vertices, dtype=numpy.float32)

        # Bind current Vertex Array Object
        # glBindVertexArray(self.VAO_id)

        # Create VBO
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        # glVertexPointer(size, GL_FLOAT, 0, None)
        glBufferData(GL_ARRAY_BUFFER, vertices.size * 4, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # Unbind VAO
        # glBindVertexArray(0)

        self.VBOs.append((VBO, size))

        return VBO

    def UseVBO(self, VBO):
        for VBO_id, size in self.VBOs:
            if (VBO_id == VBO):
                glBindBuffer(GL_ARRAY_BUFFER, VBO_id)
                
                if self.shader:
                    position = glGetAttribLocation(self.shader.shader, "position")
                    glVertexAttribPointer(position, size, GL_FLOAT, GL_FALSE, 0, None)
                    glEnableVertexAttribArray(position)
                else:
                    glVertexPointer(size, GL_FLOAT, 0, None)
                continue

    def GenerateEBO(self, indices, mode, VBO_id):
        '''
        Args:
            indices (list) : List of indices to be added in EBO.
            mode (GL constant) : GL_TRIANGLES or GL_QUAD.
            VBO_id : VBO buffer id which is binded with the indices.

        Returns:
            Buffers id.
        '''

        # cast indices to numpy array
        indices = numpy.array(indices, dtype=numpy.uint32)

        # Bind current Vertex Array Object
        # glBindVertexArray(self.VAO_id)

        # Create EBO from indices
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.size * 4, indices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        # Unbind VAO
        # glBindVertexArray(0)

        self.EBOs.append((EBO, mode, indices.size, VBO_id))

        return EBO, mode, indices.size, VBO_id

    def render(self):

        # Bind current Vertex Array Object
        # glBindVertexArray(self.VAO_id)

        if self.shader:
            self.shader.use(self.tint_color)
        else:
            glColor(*self.tint_color)

        # Draw each EBO
        for EBO_id, mode, size, VBO_id in self.EBOs:
            self.UseVBO(VBO_id)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_id)
            glDrawElements(mode, size, GL_UNSIGNED_INT, None)
            
        if self.shader:
            glUseProgram(0)

        # Unbind VAO
        # glBindVertexArray(0)

class Shader:

    def __init__(self, vertex_shader, fragment_shader):
        # Generate VAO
        # self.VAO_id = glGenVertexArrays(1)
        # glBindVertexArray(self.VAO_id)

        self.shader_vertex = compileShader(vertex_shader, GL_VERTEX_SHADER)
        self.shader_fragment = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        self.shader = compileProgram(self.shader_vertex, self.shader_fragment)
        self.mat_identity = TransformationMatrix()
        self.mat_identity.set_identity()

        
    def use(self, tint_color: tuple):
        if self.shader:
            # Bind current Vertex Array Object
            # glBindVertexArray(self.VAO_id)
            glUseProgram(self.shader)
            colorLoc = glGetUniformLocation(self.shader, "color")
            glUniform4fv(colorLoc, 1, tint_color)

            transformLoc = glGetUniformLocation(self.shader, "transform")
            mat = numpy.array([
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1,
            ], dtype=numpy.float32).reshape(4, 4)

            # set gl Matrix
            glUniformMatrix4fv(transformLoc, 1, GL_FALSE, mat)
