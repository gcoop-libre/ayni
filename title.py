# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pygame
import scene
import common
import group
import title_sprite

class Title(scene.Scene):

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.sprites = group.Group()
        self.background = common.load("title_background.png", False)
        self.title = title_sprite.TitleSprite()
        self.sprites.add(self.title)
        self.draw_background()

    def draw_background(self):
        self.world.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def update(self):
        self.sprites.update()

    def draw(self, screen):
        self.sprites.clear(screen, self.background)
        pygame.display.update(self.sprites.draw(screen))

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.KEYDOWN:
            pass
