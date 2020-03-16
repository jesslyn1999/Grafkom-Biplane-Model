from LSEngine.Behaviour import Component
from abc import ABC, abstractmethod
import random
import LSEngine
from LSEngine.Primitives import Transform, Vector
from LSEngine.Mesh import Texture, Material
import OpenGL.GL as GL
from LSEngine.Primitives.Extractable import IExtractable, Value, RandomValue
from enum import Enum
import math
from .ParticleModifiers import ParticleModifier

class EmissionShape(ABC):

    @abstractmethod
    def new_position(self):
        '''
        Returns:
            position: tuple(float, float, float) as the position
            direction: tuple(float, float, float) as the direction
        '''
        pass

class ConeShape(EmissionShape):

    def __init__(self, bottom_radius, top_radius, height):
        self.bottom_radius = bottom_radius
        self.top_radius = top_radius
        self.height = height
    
    def new_position(self):
        drad = (self.top_radius - self.bottom_radius)
        x = random.uniform(0, self.height)
        radius = (x / self.height * drad) + self.bottom_radius
        y = random.uniform(-radius, radius)
        z = random.uniform(-radius, radius)
        dx = 1
        dy = 0
        dz = 0
        if drad != 0:
            dy = (y - self.bottom_radius) / drad 
            dz = (z - self.bottom_radius) / drad
        dx, dy, dz = Vector.Normalize((dx, dy, dz))
        return Vector(x, y, z), Vector(dx, dy, dz)

class BoxShape(EmissionShape):

    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height

    def new_position(self):
        x = random.uniform(-self.width/2, self.width/2)
        y = random.uniform(-self.height/2, self.height/2)
        z = random.uniform(-self.length/2, self.length/2)
        dx = 1
        dy = 0
        dz = 0
        return Vector(x, y, z), Vector(dx, dy, dz)

class EmissionMode(Enum):

    CONTINUOUS = 0
    BURST = 1
    MOVEMENT = 2

class Particle:

    def __init__(self, size, position, rotation, velocity, angular_velocity, lifetime, tintcolor=(1, 1, 1, 1)):
        self.size = size
        self.width_modifier = 1
        self.height_modifier = 1
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.lifetime = lifetime
        self.elapsed = 0
        self.tintcolor = tintcolor

    def update(self, delta):
        self.position += self.velocity * delta
        self.rotation += self.angular_velocity * delta
        self.elapsed += delta

    def translate(self, x, y, z):
        delta = Vector(x, y, z)
        self.position += delta

    def rotate(self, angle):
        self.rotation += angle

class ParticleSystem(Component):
    
    def __init__(self, **kwargs):
        params = {
            'max_count': 10,
            'duration': Value(5),
            'spawn_rate': Value(10),
            'emission_mode': EmissionMode.CONTINUOUS,
            'initial_size': Value(1),
            'initial_velocity': Value(1),
            'initial_rotation': Value(0),
            'initial_angular_velocity': Value(0),
            'gravity': Vector(0, -1, 0),
            'texture': None,
            'material': None,
            'shape': None,
            'modifiers': [],
            'tintcolor': (1, 1, 1, 1),
        }
        params.update(kwargs)
        self.shape = params['shape']
        self.max_count = params['max_count']
        self.emission_mode = params['emission_mode']
        # Parse parameter, if not subclass of Extractable then wraps in Value class.
        self.duration = params['duration']
        if not isinstance(self.duration, IExtractable):
            self.duration = Value(self.duration)
        self.spawn_rate = params['spawn_rate']
        if not isinstance(self.spawn_rate, IExtractable):
            self.spawn_rate = Value(self.spawn_rate)
        self.initial_size = params['initial_size']
        if not isinstance(self.initial_size, IExtractable):
            self.initial_size = Value(self.initial_size)
        self.initial_velocity = params['initial_velocity']
        if not isinstance(self.initial_velocity, IExtractable):
            self.initial_velocity = Value(self.initial_velocity)
        self.initial_rotation = params['initial_rotation']
        if not isinstance(self.initial_rotation, IExtractable):
            self.initial_rotation = Value(self.initial_rotation)
        self.initial_angular_velocity = params['initial_angular_velocity']
        if not isinstance(self.initial_angular_velocity, IExtractable):
            self.initial_angular_velocity = Value(self.initial_angular_velocity)
        self.elapsed = 0
        self.gravity = params['gravity']
        self.texture = params['texture']
        self.material = params['material']
        self.particles = []
        self.modifiers = []
        for mod in params['modifiers']:
            if isinstance(mod, ParticleModifier):
                self.modifiers.append(mod)
            else:
                raise TypeError("type '{}' does not inherit from class {}".format(mod.__class__.__name__, ParticleModifier.__name__))
        self.last_pos = None
        self.tintcolor = params['tintcolor']

    def clone(self):
        return ParticleSystem(
            **self.__dict__
        )

    def spawn_particle(self):
        if self.shape:
            position, direction = self.shape.new_position()
        else:
            position = Vector(0, 0, 0)
            direction = Vector(1, 0, 0)
        wp = self.owner.transform.world_position()
        position = Vector(*((self.owner.transform.rotational_matrix * position.vector)[:-1]))
        direction = Vector(*((self.owner.transform.rotational_matrix * direction.vector)[:-1]))
        position += wp
        particle = Particle(self.initial_size.get_value(),
            position, self.initial_rotation.get_value(),
            direction * self.initial_velocity.get_value(),
            self.initial_angular_velocity.get_value(),
            self.duration.get_value(),
            self.tintcolor
        )
        self.particles.append(particle)

    def update(self):
        delta = LSEngine.delta_time()
        delta_count = self.max_count - len(self.particles)
        i = 0
        # Removes expired particles.
        while i < len(self.particles):
            if self.particles[i].elapsed > self.particles[i].lifetime:
                del self.particles[i]
            else:
                i += 1
        if delta_count > 0:
            rate = self.spawn_rate.get_value()
            if self.emission_mode == EmissionMode.CONTINUOUS:
                self.elapsed += delta
                rate_delta = 1 / rate
                rate = int(self.elapsed / rate_delta)
                self.elapsed %= rate_delta
            elif self.emission_mode == EmissionMode.MOVEMENT:
                if self.last_pos:
                    delta = self.owner.transform.position - self.last_pos
                    delta = Vector.LengthOf(delta)
                    rate = delta * rate
                else:
                    rate = 0
            spawn_count = min(delta_count, rate)
            for _ in range(0, spawn_count):
                self.spawn_particle()
        for particle in self.particles:
            particle.velocity += self.gravity * delta
            particle.update(delta)
            for modifier in self.modifiers:
                modifier.update_particle(delta, particle)
        self.last_pos = self.owner.transform.position

    def render_particle(self, particles):
        GL.glPushMatrix()
        # Resets matrix to only position.
        GL.glLoadIdentity()
        LSEngine.camera.matrix.apply()
        # GL.glTranslate(*(-v for v in LSEngine.camera.position))
        for particle in particles:
            GL.glPushMatrix()
            GL.glTranslate(*particle.position.vector)
            GL.glRotated(LSEngine.camera.rotation[1], 0, -1, 0)
            GL.glRotated(LSEngine.camera.rotation[0], 1, 0, 0)
            GL.glRotated(LSEngine.camera.rotation[2], 0, 0, 1)
            GL.glScale(particle.size * particle.width_modifier, particle.size * particle.height_modifier, 1)
            GL.glRotated(particle.rotation, 0, 0, -1)
            GL.glColor(*particle.tintcolor)

            GL.glBegin(GL.GL_QUADS)
            GL.glVertex(-0.5, -0.5, 0)
            GL.glVertex(0.5, -0.5, 0)
            GL.glVertex(0.5, 0.5, 0)
            GL.glVertex(-0.5, 0.5, 0)
            GL.glEnd()
            
            GL.glPopMatrix()

        # Rollback matrix.
        GL.glPopMatrix()

    def render_textured_particle(self, particles):
        GL.glPushMatrix()
        # Resets matrix to only position.
        GL.glLoadIdentity()
        LSEngine.camera.matrix.apply()
        # GL.glTranslate(*(v for v in LSEngine.camera.position))
        GL.glDepthMask(GL.GL_FALSE)
        for particle in particles:
            GL.glPushMatrix()
            GL.glTranslate(*particle.position.vector)
            GL.glRotated(LSEngine.camera.rotation[1], 0, -1, 0)
            GL.glRotated(LSEngine.camera.rotation[0], 1, 0, 0)
            GL.glRotated(LSEngine.camera.rotation[2], 0, 0, 1)
            GL.glScale(particle.size * particle.width_modifier, particle.size * particle.height_modifier, 1)
            GL.glRotated(particle.rotation, 0, 0, -1)
            GL.glColor(*particle.tintcolor)

            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord(0, 1)
            GL.glVertex(-0.5, -0.5, 0)
            GL.glTexCoord(1, 1)
            GL.glVertex(0.5, -0.5, 0)
            GL.glTexCoord(1, 0)
            GL.glVertex(0.5, 0.5, 0)
            GL.glTexCoord(0, 0)
            GL.glVertex(-0.5, 0.5, 0)
            GL.glEnd()

            GL.glPopMatrix()

        # Rollback matrix.
        GL.glPopMatrix()
        GL.glDepthMask(GL.GL_TRUE)

    def post_render(self):
        renderer = self.render_particle
        if self.texture:
            self.texture.use()
            renderer = self.render_textured_particle
        if self.material:
            self.material.use()
        renderer(self.particles)
        if self.material:
            self.material.unuse()
        if self.texture:
            self.texture.unuse()