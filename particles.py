import random
import pygame as pg
from entity import MoveableEntity
from settings import *


class ParticleSystem(MoveableEntity):
    def __init__(self, pos, size, groups, time, particles):
        surface = pg.Surface(size, pg.SRCALPHA)
        super(ParticleSystem, self).__init__([surface], pos, groups, 1)
        self.pos = pg.math.Vector2(self.pos.x - size[0] // 2, self.pos.y - size[1] // 2)
        self.particles = []
        self.total_particles = particles

        self.timer = 0
        self.total_time = time

    def start(self):
        pass

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        for particle in self.particles:
            self.image.blit(particle.image, particle.pos)

    def physics(self):
        for particle in self.particles:
            velocity = (particle.velocity.x, particle.velocity.y + (particle.gravity * (self.delta_time / RELATION_DELTA_TIME)))
            particle.set_velocity(velocity)
            particle.set_pos(particle.pos + particle.velocity * (self.delta_time / RELATION_DELTA_TIME))
            particle.set_fade(particle.fade - self.delta_time * 0.2)

    def delete_particles(self):
        for particle in self.particles:
            self.particles.remove(particle)
            del particle

    def update(self, delta_time):
        self.delta_time = delta_time
        self.timer += self.delta_time
        self.physics()
        self.draw()

        if self.timer > self.total_time * SECOND:
            self.delete_particles()
            self.groups().clear()
            self.kill()


class PlayerParticleSystem(ParticleSystem):
    PARTICLE = pg.transform.scale(pg.image.load("images/particle.png"), (9, 9))

    def __init__(self, pos, size, groups, time, particles):
        super(PlayerParticleSystem, self).__init__(pos, size, groups, time, particles)

    def start(self):
        for index in range(self.total_particles):
            pos = (self.image.get_width() // 2, self.image.get_height() // 2)
            velocity = (random.uniform(-2, 2), random.uniform(-1, -3))
            self.particles.append(Particle(PlayerParticleSystem.PARTICLE, pos, 0.2, velocity))

class SlimeParticleSystem(ParticleSystem):
    PARTICLE = pg.transform.scale(pg.image.load("images/particle.png"), (9, 9))

    def __init__(self, pos, size, groups, time, particles):
        super(SlimeParticleSystem, self).__init__(pos, size, groups, time, particles)

    def start(self):
        for index in range(self.total_particles):
            pos = (self.image.get_width() // 2, self.image.get_height() // 2)
            velocity = (random.uniform(-0.5, 0.5), random.uniform(-0.5, -3))
            self.particles.append(Particle(SlimeParticleSystem.PARTICLE, pos, 0.2, velocity))


class Particle:
    def __init__(self, img, pos, gravity, velocity):
        self.image = img
        self.pos = pg.math.Vector2(pos)
        self.gravity = gravity
        self.velocity = pg.math.Vector2(velocity)
        self.fade = 255

    def set_pos(self, values):
        self.pos = pg.math.Vector2(values)

    def set_velocity(self, values):
        self.velocity = pg.math.Vector2(values)

    def set_fade(self, value):
        self.fade = value
        self.image.set_alpha(self.fade)
