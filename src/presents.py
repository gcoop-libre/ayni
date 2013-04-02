# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import pygame
import scene
import config
import common
import group
import title_sprite
import game
import intro
import common
import pytweener
import menu
from sprite import Sprite

class Presents(scene.Scene):
    "Muestra el logotipo de gcoop y el texto: 'presenta...'"

    def __init__(self, world):
        pygame.mixer.init()
        common.play_music('intro.wav')
        scene.Scene.__init__(self, world)
        self.sprites = group.Group()
        self.background = common.load("presents/background.png", False, (config.WIDTH, config.HEIGHT))
        self.gcoop = GcoopLogo()
        self.presents = PresentsText()
        self.sprites.add(self.gcoop)
        self.draw_background()
        self.counter = 0

    def draw_background(self):
        self.world.screen.fill((255, 255, 255))
        self.world.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def update(self):
        self.sprites.update()
        self.counter += 1

        if self.counter == 90:
            self.presents.start()
            self.sprites.add(self.presents)
        elif self.counter > 200:
            self.go_to_intro_scene()

    def draw(self, screen):
        self.sprites.clear(screen, self.background)
        pygame.display.update(self.sprites.draw(screen))

    def on_event(self, event):
        if self.counter > 50:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.go_to_intro_scene()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.go_to_menu_inmediately()
                else:
                    self.go_to_intro_scene()

    def go_to_menu_inmediately(self):
        new_scene = menu.Menu(self.world)
        self.world.change_scene(new_scene)

    def go_to_intro_scene(self):
        new_scene = intro.Intro1(self.world)
        self.world.change_scene(new_scene)

class PresentsText(Sprite):
    "El texto de indica: 'presents'"

    def __init__(self):
        Sprite.__init__(self)
        self.image = common.load('presents/presents.png', False, (config.WIDTH * 0.3, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = config.WIDTH / 2
        self.rect.y = config.HEIGHT * 0.8
        self.alpha = 0
        self.update()

    def start(self):
        common.tweener.addTween(self, alpha=255, tweenTime=500,
                tweenType=pytweener.Easing.Linear.easeNone)

    def update(self):
        if self.alpha != 128:
            self.image.set_alpha(self.alpha)

class GcoopLogo(Sprite):
    "El logotipo de gcoop."

    def __init__(self):
        Sprite.__init__(self)
        self.original_image = common.load('presents/gcoop.png', False, (int(config.WIDTH * 0.6), 0))
        self.image = self.original_image
        self.alpha = 0
        self.rect = self.image.get_rect()
        self.rect.centerx = config.WIDTH / 2
        self.center = self.rect.center
        self.y = config.HEIGHT * 0.1
        w, h = self.image.get_width(), self.image.get_height()
        self.width = 0
        self.height = 0

        common.tweener.addTween(self, width=w, tweenTime=1700,
                tweenType=pytweener.Easing.Elastic.easeInOut)
        common.tweener.addTween(self, height=h, tweenTime=1800,
                tweenType=pytweener.Easing.Elastic.easeInOut)
        common.tweener.addTween(self, alpha=255, tweenTime=500,
                tweenType=pytweener.Easing.Linear.easeNone)
        self.update()


    def update(self):
        self.rect.y = self.y
        new_size = (max(0, int(self.width)), max(0, int(self.height)))

        self.image = pygame.transform.scale(self.original_image, new_size)

        # evita un bug de pygame en mi equipo, una imagen
        # con transparencia a la mitad exacta produce un
        # interlineado feo...
        if self.alpha != 128:
            self.image.set_alpha(self.alpha)
        else:
            self.image.set_alpha(127)

        self.rect.width = self.width
        self.rect.center = (config.WIDTH / 2, config.HEIGHT * 0.4)
