# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from sprite import Sprite
import common
import random

class Nubes:
    """Muestra un montón de nubes moviendose por el fondo."""

    def __init__(self, sprites):
        self.sprites = sprites
        self.nubes = []
        imagenes = [common.load("nubes/1.png", True),
                    common.load("nubes/2.png", True),
                    common.load("nubes/3.png", True)]

        velocidades = [0.1, 0.2, 0.3, 0.4]

        for x in range(8):
            nube = Nube(random.choice(imagenes), random.choice(velocidades))
            self.nubes.append(nube)
            self.sprites.add(nube)

    def update(self):
        for x in self.nubes:
            x.update()

class Nube(Sprite):

    def __init__(self, imagen, velocidad):
        self.image = imagen
        Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.x = random.randint(-50, 1000)
        self.rect.y = random.randint(-20, 600)
        self.velocidad = velocidad

    def update(self):
        self.rect.x = self.x
        self.x += self.velocidad

        if self.x > 1200:
            self.x = -self.rect.width
