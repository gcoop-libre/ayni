# -*- encoding: utf-8 -*-
import pygame
import random
import sys
import animation

class World:

    def __init__(self):
        "Inicializa la biblioteca y el modo de video."

        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Ayni")
        pygame.font.init()

    def loop(self):
        clock = pygame.time.Clock()

        quit = False

        while not quit:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        quit = True

                # delega los eventos a la escena.
                self.scene.on_event(event)

            # delega actualizacion e impresión a la escena.
            self.scene.update()
            self.scene.draw(self.screen)

            clock.tick(60)

    def change_scene(self, new_scene):
        self.scene = new_scene
