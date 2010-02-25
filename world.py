# -*- encoding: utf-8 -*-
import pygame
import random
import sys
import animation
import common
import time

class World:
    "Representa el administrador de escenas y el bucle de juego."

    def __init__(self):
        "Inicializa la biblioteca y el modo de video."

        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Ayni")
        pygame.font.init()

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
