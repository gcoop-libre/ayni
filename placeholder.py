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
import config

class Placeholder(Sprite):
    "Representa un bloque para completar."

    def __init__(self, type, x, y):
        Sprite.__init__(self)

        if config.SHOW_PLACEHOLDERS:
            self.image = common.load('placeholder.png', True)
        else:
            self.image = common.load('hide.png', True)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.are_used = False
        self.is_floor = False

        self.rect.width = 75
        self.rect.height = 75
        self.type = type
