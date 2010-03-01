# -*- coding: utf-8 -*-
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
