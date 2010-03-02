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


class Pipe(Sprite, object):
    "Representa una pieza del juego."

    def __init__(self, game, type, x, y, map):
        Sprite.__init__(self)
        self.type = type
        self.image = common.load('front_pipes/%d.png' %(type), True)
        self.rect = self.image.get_rect()
        self.map = map
        self.can_be_clicked = True
        self.x = x - self.rect.w / 2
        self.y = y - self.rect.h
        self.are_in_a_placeholder = False
        self.z = -10
        self.game = game

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def move_to(self, x, y):
        common.tweener.addTween(self, x=x, tweenTime=700)
        common.tweener.addTween(self, y=y, tweenTime=700)

    def put_in_this_placeholder(self, placeholder):
        self.x = placeholder.rect.x
        self.y = placeholder.rect.y
        self.are_in_a_placeholder = True
        self.placeholder = placeholder
        self.placeholder.are_used = True

        if self.type in [2, 8]:
            self.placeholder.is_floor = True
        else:
            self.placeholder.is_floor = False

    def get_placeholder(self):
        if self.are_in_a_placeholder:
            return self.placeholder
        else:
            raise Exception("El pipe no esta en un placeholder")

    def remove_from_a_placeholder(self):
        self.are_in_a_placeholder = False
        self.placeholder.are_used = False
        del(self.placeholder)

    def is_in_a_right_placeholder(self):
        "Retorna True si la pieza esta en el placeholder que le corresponde."
        same = {
                8:2,
                2:8,
                4:6,
                6:4,
                }
                
        if self.type == self.placeholder.type:
            return True
        elif same.has_key(self.type) and same[self.type] == self.placeholder.type:
            return True
        else:
            return False
