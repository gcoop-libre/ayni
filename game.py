# -*- coding: utf-8 -*-
import pygame
import scene
import common
import map
import mouse
import player

class Game(scene.Scene):

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.map = map.Map()
        self._draw_background_and_map()
        self.sprites = pygame.sprite.OrderedUpdates()

        self._create_player()
        self._create_mouse_pointer()

    def _create_mouse_pointer(self):
        m = mouse.MousePointer([])
        self.sprites.add(m)

    def _create_player(self):
        p = player.Player(603, 478, self.map)
        self.sprites.add(p)

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
        pass
