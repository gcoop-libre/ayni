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
        self.type = type
        self.image = common.load('front_pipes/%d.png' %(type), True)
        self.rect = self.image.get_rect()
        self.map = map
        self.can_be_clicked = True
        self.x = x - self.rect.w / 2
        self.y = y - self.rect.h
        self.are_in_a_placeholder = False
        self.z = -10

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
