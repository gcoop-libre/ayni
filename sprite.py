# -*- coding: utf-8 -*-
import pygame

class Sprite(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.can_be_dragged = False

    def collide_with(self, x, y):
        return self.rect.collidepoint(x, y)
