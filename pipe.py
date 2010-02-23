# -*- coding: utf-8 -*-
import pygame
import random
import sys
import animation
import common
from states import *
from sprite import Sprite


class Pipe(Sprite):
    "Representa un personaje del juego."

    def __init__(self, type, x, y, map):
        Sprite.__init__(self)
        self.image = common.load('front_pipes/%d.png' %(type), True)
        self.rect = self.image.get_rect()
        self.rect.move_ip((x - self.rect.w / 2, y - self.rect.h))
        self.map = map
        self.can_be_dragged = True

    def update(self):
        pass
