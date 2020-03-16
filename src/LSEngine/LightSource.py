from OpenGL.GL import *
from .Behaviour import Component
from .Primitives import TransformationMatrix
import math

light_ids = [GL_LIGHT0, GL_LIGHT1, GL_LIGHT2, GL_LIGHT3, GL_LIGHT4, GL_LIGHT5, GL_LIGHT6, GL_LIGHT7]

class SpotLight(Component):

    def __init__(self, l_id, amb, diff, spec, exp, cut):
        self.id = l_id
        self.ambient = amb
        self.diffuse = diff
        self.specular = spec
        self.exponent = exp
        self.cutoff = cut

    def clone(self):
        return SpotLight(self.id + 1, self.ambient, self.diffuse, self.specular, self.exponent, self.cutoff)

    def pre_render(self):
        self.update_parameters()

    def update_parameters(self):
        light_const = light_ids[self.id]
        
        direction = [1, 0, 0]
        direction = TransformationMatrix.rotate(self.owner.transform.rotation[0], (-1, 0, 0)) * direction
        direction = TransformationMatrix.rotate(self.owner.transform.rotation[1], (0, -1, 0)) * direction
        direction = TransformationMatrix.rotate(self.owner.transform.rotation[2], (0, 0, -1)) * direction
        pos = (*self.owner.transform.position, 1)
        glLightfv(light_const, GL_POSITION, pos)
        glLightfv(light_const, GL_AMBIENT, self.ambient)
        glLightfv(light_const, GL_DIFFUSE, self.diffuse)
        glLightfv(light_const, GL_SPECULAR, self.specular)
        glLightfv(light_const, GL_SPOT_DIRECTION, direction)
        glLightf(light_const, GL_SPOT_EXPONENT, self.exponent)
        glLightf(light_const, GL_SPOT_CUTOFF, self.cutoff)
        glLightf(light_const, GL_CONSTANT_ATTENUATION, 1)
        glLightf(light_const, GL_LINEAR_ATTENUATION, 0)
        glLightf(light_const, GL_QUADRATIC_ATTENUATION, 0)

    def on_enabled(self):
        light_const = light_ids[self.id]

        glEnable(light_const)
        self.update_parameters()

    def on_disabled(self):
        glDisable(light_ids[self.id])

        