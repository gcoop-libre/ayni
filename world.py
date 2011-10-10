# -*- encoding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pygame
import random
import sys
import animation
import common
import time
import audio
import config
import cPickle
import os

class World:
    "Representa el administrador de escenas y el bucle de juego."

    def __init__(self, in_sugar_olpc=False):
        "Inicializa la biblioteca y el modo de video."

        if config.FULLSCREEN:
            flags = pygame.FULLSCREEN
        else:
            flags = 0

        if config.LOWRES:
            resolution = (640, 720 / 2)
        else:
            resolution = (1200, 846)

        if in_sugar_olpc:
            self.screen = pygame.display.get_surface()
        else:
            self.screen = pygame.display.set_mode(resolution, flags)

        self.in_sugar_olpc = in_sugar_olpc
        pygame.display.set_caption("Ayni")
        pygame.font.init()
        self.audio = audio.Audio()
        self.runtime = 0

    def loop(self):
        "Bucle principal que actualiza escenas y mantiene la velocidad constante."
        clock = pygame.time.Clock()
        clock.tick(60)
        clock.get_time()
        save_events = False

        quit = False

        while not quit:
            self.runtime += clock.get_time()

            if self.in_sugar_olpc:
                import gtk
                while gtk.events_pending():
                    gtk.main_iteration()


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    print event
                    quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                    elif event.key == pygame.K_F12:
                        self.take_screenshot()
                    elif event.key in [pygame.K_f, pygame.K_F3]:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_r:
                        print "Comenzando a grabar los eventos..."
                        save_events = True
                        self.runtime = 0
                        events = []
                    elif event.key == pygame.K_s:
                        if save_events:
                            print "Terminando la grabacion de eventos..."

                            f = open("events.txt", "wt")
                            cPickle.dump(events, f)
                            f.close()

                        else:
                            print "No estaba grabando con anterioridad."

                # delega los eventos a la escena.
                if save_events:
                    if event.type == pygame.MOUSEMOTION:
                        events.append((self.runtime, event.type,
                            dict(buttons=event.buttons, pos=event.pos,
                                rel=event.rel)))
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        events.append((self.runtime, event.type, 
                            dict(button=event.button, pos=event.pos)))


                self.scene.on_event(event)

            # delega actualizacion e impresión a la escena.
            self.scene.update()
            self.scene.draw(self.screen)

            common.tweener.update(16)
            clock.tick(60)

    def change_scene(self, new_scene):
        self.scene = new_scene

    def take_screenshot(self):
        self.scene.draw(self.screen)
        filename = time.strftime("screenshot_%y%m%d_%H%M%S.png")
        pygame.image.save(self.screen, filename)
        print "Guardando:", filename
    
    def next_level(self, level):
        level += 1
        if os.path.isfile('data/map/%d.txt' % level):
            return level
