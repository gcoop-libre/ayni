# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import pygame
import common
import pytweener
import random

class Particle:
    "Es una particula del efecto."

    def __init__(self, parent_list, x, y, vx, vy, va):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.alpha = 255
        self.va = va
        self.parent_list = parent_list
        parent_list.append(self)

    def draw(self, screen):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.alpha -= self.va

        if self.alpha <= 0:
            self.parent_list.remove(self)
            return

        rect = pygame.Rect(self.x, self.y, 2, 2)
        color = (255, 255, 255, self.alpha)
        pygame.draw.rect(screen, color, rect)
        


class Particles(pygame.sprite.Sprite):
    """Un efecto de particulas para representar el aplique de pieza."""

    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = common.load("particle_box.png", True)
        self.image = self.original_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = rect.center
        self.ttl = 40
        self.z = 300
        self.particles = []

    def create_particles(self):
        for x in range(10):
            Particle(self.particles, 100, 100, random.randint(-3, 3), random.randint(-6, 2), 2)

    def update(self):
        self.ttl -= 1

        self.image = self.original_image.convert_alpha()

        for p in self.particles:
            p.draw(self.image)

        if self.ttl < 10:
            if self.ttl < -30:
                self.kill()
            else:
                return
        else:
            if self.ttl % 11 == 0:
                self.create_particles()
