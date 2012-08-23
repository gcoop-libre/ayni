# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pygame
import scene

class Transition(scene.Scene):
    "Muestra una transición entre una etapa de la presentación y la otra."

    def __init__(self, world, last_scene, new_scene):
        self.counter = 0
        self.new_scene = new_scene
        self.last_scene = last_scene
        self.world = world
        self.last_image = world.screen.convert()
        self.new_scene.draw_background(world.screen)
        self.counter = 255

    def update(self):
        self.counter -= 4

        if self.counter < 0:
            self.set_new_scene()

    def draw(self, screen):
        self.new_scene.draw_background(screen)
        self.last_image.set_alpha(self.counter)
        screen.blit(self.last_image, (0, 0))
        pygame.display.flip()

    def set_new_scene(self):
        self.world.change_scene(self.new_scene)

    def on_event(self, event):
        self.new_scene.on_event(event)
