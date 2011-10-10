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
import transition


class IntroAbstract(scene.Scene):
    "Representa una etapa de la presentación, por ejemplo la primer imagen."

    def __init__(self, world, image, next_scene, must_interpolate=True):
        scene.Scene.__init__(self, world)
        self.background = common.load(image, False)
        self.counter = 0
        self.next_scene = next_scene
        self.must_interpolate = must_interpolate

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def update(self):
        self.counter += 1

        if self.counter > 400:
            self.go_to_next_scene()

    def draw(self, screen):
        pygame.display.flip()

    def on_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.go_to_next_scene()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_to_title_scene()
            else:
                self.go_to_next_scene()

    def go_to_title_scene(self):
        self.world.change_scene(title.Title(self.world))
                
    def go_to_next_scene(self):
        next_scene = self.next_scene(self.world)
        last_scene = self

        if self.must_interpolate:
            self.world.change_scene(transition.Transition(self.world, last_scene, next_scene))
        else:
            self.world.change_scene(next_scene)


class Intro1(IntroAbstract):
    "Muestra una escena de la presentación: la casa sin agua."

    def __init__(self, world):
        IntroAbstract.__init__(self, world, "intro/1.jpg", Intro2)
        self.draw_background(world.screen)
        

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
        IntroAbstract.__init__(self, world, "intro/5.jpg", title.Title, False)
