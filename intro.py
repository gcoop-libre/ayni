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
import title


class IntroAbstract(scene.Scene):
    "Representa una etapa de la presentación, por ejemplo la primer imagen."

    def __init__(self, world, image, next_scene):
        scene.Scene.__init__(self, world)
        self.background = common.load(image, False)
        self.counter = 0
        self.draw_background()
        self.next_scene = next_scene

    def draw_background(self):
        self.world.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def update(self):
        self.counter += 1

        if self.counter > 400:
            self.go_to_next_scene()

    def draw(self, screen):
        pass

    def on_event(self, event):

        if self.counter > 50:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.go_to_next_scene()
                
    def go_to_next_scene(self):
        self.world.change_scene(self.next_scene(self.world))



class Intro1(IntroAbstract):
    "Muestra una escena de la presentación: la casa sin agua."

    def __init__(self, world):
        IntroAbstract.__init__(self, world, "intro/1.jpg", Intro2)
        

class Intro2(IntroAbstract):
    "Muestra una escena de la presentación: las personas viendo la casa."

    def __init__(self, world):
        IntroAbstract.__init__(self, world, "intro/2.jpg", Intro3)
        
        
class Intro3(IntroAbstract):
    "Muestra una escena de la presentación: sugiere una cooperativa."

    def __init__(self, world):
        IntroAbstract.__init__(self, world, "intro/3.jpg", Intro4)


class Intro4(IntroAbstract):
    "Muestra una escena de la presentación: gente dando ideas."

    def __init__(self, world):
        IntroAbstract.__init__(self, world, "intro/4.jpg", Intro5)


class Intro5(IntroAbstract):
    "Muestra una escena de la presentación: dos cooperativistas comenzando."

    def __init__(self, world):
        IntroAbstract.__init__(self, world, "intro/5.jpg", title.Title)

