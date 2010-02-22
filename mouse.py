# -*- coding: utf-8 -*-
import pygame
import random
import sys
import animation
import common

Sprite = pygame.sprite.Sprite

class MousePointer(Sprite):

    def __init__(self, stage_objects):
        pygame.sprite.Sprite.__init__(self)
        pygame.mouse.set_visible(False)
        self._load_frames()
        self.show()
        self.set_frame('normal')
        self.rect = self.image.get_rect()
        self.stage_objects = stage_objects

    def _load_frames(self):
        self.frames = {
                'normal': common.load("mouse.png", True),
                'over': common.load("over.png", True),
                'hide': common.load("hide.png", True),
                }

    def set_frame(self, name):
        self.image = self.frames[name]

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()

        if self.visible:
            if self.are_over_any_stage_object():
                self.set_frame("over")
            else:
                self.set_frame("normal")

    def are_over_any_stage_object(self):
        x, y = self.rect.topleft
        for sprite in self.stage_objects:
            if sprite.can_click_it(x, y):
                return True

    def hide(self):
        self.visible = False
        self.set_frame("hide")

    def show(self):
        self.visible = True
        self.set_frame("normal")
