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
import intro
from sprite import Sprite
import common
import pytweener

class Presents(scene.Scene):
    "Muestra el logotipo de gcoop y el texto: 'presenta...'"

    def __init__(self, world):
        pygame.mixer.init()
        pygame.mixer.music.load('data/presents/music.ogg')
        #music = pygame.mixer.Sound('presents/music.ogg')
        #music.play()
        pygame.mixer.music.play()
        scene.Scene.__init__(self, world)
        self.sprites = group.Group()
        self.background = common.load("presents/background.png", False)
        self.gcoop = GcoopLogo()
        self.presents = PresentsText()
        self.sprites.add(self.gcoop)
        self.draw_background()
        self.counter = 0

    def draw_background(self):
        self.world.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def update(self):
        self.sprites.update()
        self.counter += 1

        if self.counter == 100:
            self.presents.start()
            self.sprites.add(self.presents)
        elif self.counter > 400:
            self.go_to_intro_scene()

    def draw(self, screen):
        self.sprites.clear(screen, self.background)
        pygame.display.update(self.sprites.draw(screen))

    def on_event(self, event):
        if self.counter > 50:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.go_to_intro_scene()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_SPACE]:
                    self.go_to_game_inmediately()
                else:
                    self.go_to_intro_scene()

    def go_to_game_inmediately(self):
        import game
        new_scene = game.Game(self.world)
        self.world.change_scene(new_scene)
        

    def go_to_intro_scene(self):
        new_scene = intro.Intro1(self.world)
        self.world.change_scene(new_scene)

class PresentsText(Sprite):
    "El texto de indica: 'presents'"

    def __init__(self):
        Sprite.__init__(self)
        self.image = common.load('presents/presents.png', False)
        self.rect = self.image.get_rect()
        self.rect.centerx = 1280 / 2
        self.rect.y = 600
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
        self.original_image = common.load('presents/gcoop.png', False)
        self.image = self.original_image
        self.alpha = 0
        self.rect = self.image.get_rect()
        self.rect.centerx = 1260 / 2
        self.center = self.rect.center
        self.y = 90
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
        new_size = (int(self.width), int(self.height))

        if new_size[0] < 0:
            new_size = 0, new_size[1]

        if new_size[1] < 0:
            new_size = new_size[0], 0

        self.image = pygame.transform.scale(self.original_image, new_size)

        # evita un bug de pygame en mi equipo, una imagen
        # con transparencia a la mitad exacta produce un
        # interlineado feo...
        if self.alpha != 128:
            self.image.set_alpha(self.alpha)
        else:
            self.image.set_alpha(127)

        self.rect.width = self.width
        self.rect.center = (600, 260)
