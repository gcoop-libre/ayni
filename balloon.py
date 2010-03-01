# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from sprite import Sprite
import common

class Balloon(Sprite):
    "Un globo que tiene texto representando lo que dice un personaje."

    def __init__(self, text_image, x, y):
        Sprite.__init__(self)
        self.image = common.load('balloon.png', True)
        self.rect = self.image.get_rect()
        self.rect.right = x + 70
        self.rect.bottom = y
        self.time_to_live = 150
        self.image.blit(text_image, (5, 5))

        # Evita que el cuadro de dialogo salga de la pantalla
        if self.rect.left < 2:
            self.rect.left = 2
        elif self.rect.right > 638:
            self.rect.right = 638

    def update(self):
        self.time_to_live -= 1

        if self.time_to_live < 0:
            self.kill()
