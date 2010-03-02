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

class World:
    "Representa el administrador de escenas y el bucle de juego."

    def __init__(self):
        "Inicializa la biblioteca y el modo de video."

        if config.FULLSCREEN:
            flags = pygame.FULLSCREEN
        else:
            flags = 0

        self.screen = pygame.display.set_mode((1280, 720), flags)
        pygame.display.set_caption("Ayni")
        pygame.font.init()
        self.audio = audio.Audio()

    def loop(self):
        "Bucle principal que actualiza escenas y mantiene la velocidad constante."
        clock = pygame.time.Clock()

        quit = False

        while not quit:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                    elif event.key == pygame.K_F12:
                        self.take_screenshot()
                    elif event.key in [pygame.K_f, pygame.K_F3]:
                        pygame.display.toggle_fullscreen()

                # delega los eventos a la escena.
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
