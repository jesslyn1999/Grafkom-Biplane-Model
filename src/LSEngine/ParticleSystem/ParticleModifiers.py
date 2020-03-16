from abc import ABC, abstractmethod
import noise
import time
import math
from LSEngine.Primitives.Types import Vector

class ParticleModifier(ABC):

    @abstractmethod
    def update_particle(self, delta, particle):
        pass

class ParticleSizeOverTime(ParticleModifier):

    def __init__(self, func):
        self.func = func

    def update_particle(self, delta, particle):
        stage = particle.elapsed / particle.lifetime
        if stage > 1:
            stage = 1
        elif stage < 0:
            stage = 0
        particle.size = self.func(stage)

class ParticleColorOverTime(ParticleModifier):

    def __init__(self, gradient):
        self.gradient = gradient

    def update_particle(self, delta, particle):
        stage = particle.elapsed / particle.lifetime
        if stage > 1:
            stage = 1
        elif stage < 0:
            stage = 0
        particle.tintcolor = self.gradient(stage)

class ParticleSizeOverVelocity(ParticleModifier):

    def __init__(self, width_func, height_func):
        self.width_func = width_func
        self.height_func = height_func

    def update_particle(self, delta, particle):
        if self.width_func:
            particle.width_modifier = self.width_func(particle.velocity)
        if self.height_func:
            particle.height_modifier = self.height_func(particle.velocity)

class ParticleWind(ParticleModifier):

    def __init__(self, multiplier):
        self.multiplier = multiplier
        self.t = 0
    
    def update_particle(self, delta, particle):
        self.t += delta
        if self.multiplier != 0:
            angle = noise.snoise4(
                particle.position.x,
                particle.position.y,
                particle.position.z,
                self.t
            ) * math.pi
            dx = math.cos(angle)
            dz = math.sin(angle)
            d = Vector(dx, 0, dz) * self.multiplier * delta
            particle.position += d