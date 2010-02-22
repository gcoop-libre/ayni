# -*- coding: utf-8 -*-
import pygame
import random
import sys
import animation
import common
from states import *

Sprite = pygame.sprite.Sprite

class Placeholder(Sprite):
    "Representa un bloque para completar."

    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = common.load('placeholder.png', True)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        pass
