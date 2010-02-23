# -*- coding: utf-8 -*-
import pygame
import random
import sys
import animation
import common
import mouse_state
from sprite import Sprite
import placeholder

class MousePointer(Sprite):

    def __init__(self, stage_objects):
        Sprite.__init__(self)
        pygame.mouse.set_visible(False)
        self._load_frames()
        self.show()
        self.set_frame('normal')
        self.rect = self.image.get_rect()
        self.stage_objects = stage_objects
        self.change_state(mouse_state.Normal(self))

    def _load_frames(self):
        self.frames = {
                'normal':   common.load("mouse.png", True),
                'over':     common.load("over.png", True),
                'dragging': common.load("dragging.png", True),
                'hide':     common.load("hide.png", True),
                }

    def set_frame(self, name):
        self.image = self.frames[name]

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()
        self.state.update()

    def on_click(self, x, y):
        self.state.on_click(x, y)

    def are_over_any_stage_object(self):
        x, y = self.rect.topleft
        for sprite in self.stage_objects:
            if sprite.can_be_dragged and sprite.collide_with(x, y):
                return True

    def get_object_over_mouse(self):
        x, y = self.rect.topleft
        for sprite in self.stage_objects:
            if sprite.can_be_dragged and sprite.collide_with(x, y):
                return sprite
        
    def get_placeholder_over_mouse(self):
        x, y = self.rect.topleft
        for sprite in self.stage_objects:
            if issubclass(sprite.__class__, placeholder.Placeholder) and sprite.collide_with(x, y):
                return sprite

    def hide(self):
        self.visible = False
        self.set_frame("hide")

    def show(self):
        self.visible = True
        self.set_frame("normal")

    def change_state(self, state):
        self.state = state
