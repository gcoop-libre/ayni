# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pygame
import scene
import common
import group
import game
import presents
import common

class End(scene.Scene):
    "Muestra la escena que le muestra al usuario que ha logrado el objetivo."

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.sprites = group.Group()
        self.background = common.load("end/festejo.jpg", False)
        self.draw_background()
        self.counter = 0

    def draw_background(self):
        self.world.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def update(self):
        self.counter += 1

    def draw(self, screen):
        pass

    def on_event(self, event):
        if self.counter > 100:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                new_scene = presents.Presents(self.world)
                self.world.change_scene(new_scene)
