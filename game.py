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

class Game(scene.Scene):
    """Es la escena principal del juego, donde el usuario puede
       interactuar con los trabajadores, el mouse y las piezas."""

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.sprites = group.Group()
        self.messages = messages.Messages(self.sprites)
        self.map = map.Map(self, self.sprites, self.messages, world.audio)
        self._draw_background_and_map()

        #self._create_a_pipe()
        self._create_mouse_pointer()
        self.sprites.sort_by_z()

    def _create_mouse_pointer(self):
        self.mouse = mouse.MousePointer(self.sprites)
        self.sprites.add(self.mouse)

    def _draw_background_and_map(self):
        "Imprime y actualiza el fondo de pantalla para usar dirtyrectagles mas adelante."
        self.background = common.load("background.jpg", False)
        self.map.draw_over(self.background)
        self.world.screen.blit(self.background, (0, 0))

        # actualiza toda la pantalla.
        pygame.display.flip()

    def update(self):
        self.sprites.update()

    def draw(self, screen):
        self.sprites.clear(screen, self.background)
        pygame.display.update(self.sprites.draw(screen))

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            self.mouse.on_click(x, y)

    def on_pipe_put(self):
        "Evento que activa la pieza cuando se suelta en un placeholder."

        if self.map.all_pipes_are_in_correct_placeholders():
            for x in self.map.players:
                x.show_end_level_animation()
            
            self.show_level_complete_message()

    def show_level_complete_message(self):
        "Muestra el mensaje de texto que dice 'nivel completado...'"
        self.sprites.add(level_complete.LevelComplete())
