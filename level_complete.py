# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from sprite import Sprite
import common
import pytweener

class LevelComplete(Sprite):
    "Representa el texto que le indica al jugador que ha completado el nivel."

    def __init__(self):
        Sprite.__init__(self)
        self.image = common.load('level_complete.png', True)
        self.rect = self.image.get_rect()
        self.rect.centerx = 1280 / 2
        self.y = -self.rect.h
        common.tweener.addTween(self, y=300, tweenTime=1700, 
                tweenType=pytweener.Easing.Elastic.easeInOut)

    def update(self):
        self.rect.y = self.y
