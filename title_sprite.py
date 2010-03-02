# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from sprite import Sprite
import common
import pytweener

class TitleSprite(Sprite):
    "El texto del juego que entra en la escena de presentación."

    def __init__(self):
        Sprite.__init__(self)
        self.image = common.load('title.png', True)
        self.rect = self.image.get_rect()
        self.rect.centerx = 1280 / 2
        self.y = 780
        common.tweener.addTween(self, y=40, tweenTime=1700, tweenType=pytweener.Easing.Elastic.easeInOut)

    def update(self):
        self.rect.y = self.y
