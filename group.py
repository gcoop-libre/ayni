# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import pygame
import pprint

class Group(pygame.sprite.OrderedUpdates):

    def __init__(self, *k):
        pygame.sprite.OrderedUpdates.__init__(self, *k)

    def sort_by_z(self):
        sprites = self.sprites()
        sprites.sort()
        self.empty()

        for x in sprites:
            self.add(x)
