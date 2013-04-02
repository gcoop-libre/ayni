# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from sprite import Sprite
import config
import common
import pytweener

class TitleSprite(Sprite):
    "El texto del juego que entra en la escena de presentación."

    def __init__(self):
        Sprite.__init__(self)
        self.image = common.load('title.png', True, (config.WIDTH * 0.3, 0))
        self.rect = self.image.get_rect()
        self.rect.right = config.WIDTH * 0.9
        self.y = config.HEIGHT
        common.tweener.addTween(self, y=self.y * 0.05, tweenTime=1700,
                tweenType=pytweener.Easing.Elastic.easeInOut)

    def update(self):
        self.rect.y = self.y


class StatusMessage(Sprite):
    "Muestra un mensaje indicando que tiene que pulsar una tecla para continuar"

    def __init__(self):
        Sprite.__init__(self)
        self.image = common.load('continue.png', True, (config.WIDTH * 0.7, 0))
        self.rect = self.image.get_rect()
        self.y = config.HEIGHT + self.rect.h
        self.rect.bottom = self.y
        self.rect.centerx = config.WIDTH / 2
        common.tweener.addTween(self, y=self.y * 0.9, tweenTime=1700)

    def update(self):
        self.rect.bottom = self.y
