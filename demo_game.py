# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pygame
import scene
import common
import map
import mouse
import pipe
import group
import messages
import level_complete
import particles
import end
import game
import cPickle
import pygame


class DemoGame(game.Game):
    """Es similar a la escena Game pero no espera que el usuario
       genere los eventos de entrada sino que los lee de un archivo
       de configuración."""

    def __init__(self, world):
        game.Game.__init__(self, world)
        self.events = cPickle.load(open('events.txt', "rt"))
        world.runtime = 0
        self.next_event = self.get_next_event()

    def update(self):


        if self.next_event[0] < self.world.runtime:
            event_type = self.next_event[1]
            event = self.next_event[2]
            print event_type

            if event_type == 4:
                new_event = pygame.event.Event(pygame.MOUSEMOTION, event)
                pygame.event.post(new_event)
            elif event_type == 5:
                new_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, event)
                pygame.event.post(new_event)

            self.next_event = self.get_next_event()


        game.Game.update(self)

    def draw(self, screen):
        game.Game.draw(self, screen)
        # TODO: dibujar una leyenda avisando.

    def get_next_event(self):
        if self.events:
            return self.events.pop(0)
        else:
            print "No hay mas eventos para interpretar."
            return (9999999999, 0)
