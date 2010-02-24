# -*- coding: utf-8 -*-
import pygame
import random
import sys
import animation
import common
from states import *
from sprite import Sprite


class Pipe(Sprite, object):
    "Representa una pieza del juego."

    def __init__(self, type, x, y, map):
        Sprite.__init__(self)
        self.image = common.load('front_pipes/%d.png' %(type), True)
        self.rect = self.image.get_rect()
        self.map = map
        self.can_be_clicked = True
        self.x = x - self.rect.w / 2
        self.y = y - self.rect.h

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def move_to(self, x, y):
        common.tweener.addTween(self, x=x, tweenTime=700)
        common.tweener.addTween(self, y=y, tweenTime=700)

