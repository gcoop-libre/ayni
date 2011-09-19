# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import pygame
import random
import sys
import animation
import common
from states import *
from sprite import Sprite


class SelectedArrow(Sprite, object):
    "Representa una pieza del juego."

    def __init__(self, game, map, target):
        Sprite.__init__(self)
        self._load_frames()
        self.type = type
        self.image = self.animation.get_image()
        self.rect = self.image.get_rect()
        self.map = map
        self.can_be_clicked = False
        self.rect.x = target.rect.x + (target.rect.w/2 - self.rect.w/2)
        self.rect.y = target.rect.y - target.rect.h/2
        self.z = -10
        self.game = game
        self._load_frames()
        map.sprites.add(self)
        self.target = target
    
    def _load_frames(self):
        sheet_selected = animation.Sheet(common.load("selected_arrow.png", True), 2)
        self.animation = animation.Animation(sheet_selected, 10 ,[0, 1])

    def update(self):
        self.rect.x = self.target.rect.x+self.target.rect.w/2-self.rect.w/2
        self.rect.y = self.target.rect.y-self.target.rect.h/2
        self.animation.update()
        self.image = self.animation.get_image()

    def move_to(self, x, y):
        common.tweener.addTween(self, x=x, tweenTime=700)
        common.tweener.addTween(self, y=y, tweenTime=700)


