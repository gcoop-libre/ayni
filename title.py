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
import game

class Title(scene.Scene):

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.sprites = group.Group()
        self.background = common.load("title_background.jpg", False)
        self.title = title_sprite.TitleSprite()
        self.sprites.add(self.title)
        self.draw_background()
        self.counter = 0

    def draw_background(self):
        self.world.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def update(self):
        self.sprites.update()
        self.counter += 1

        if self.counter == 50:
            self.sprites.add( title_sprite.StatusMessage())

    def draw(self, screen):
        self.sprites.clear(screen, self.background)
        pygame.display.update(self.sprites.draw(screen))

    def on_event(self, event):

        if self.counter > 50:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.world.change_scene(game.Game(self.world))
