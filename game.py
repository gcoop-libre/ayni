# -*- coding: utf-8 -*-
import pygame
import scene
import common
import map
import mouse
import player
import pipe

class Game(scene.Scene):

    def __init__(self, world):
        scene.Scene.__init__(self, world)
        self.sprites = pygame.sprite.OrderedUpdates()
        self.map = map.Map(self.sprites)
        self._draw_background_and_map()

        self._create_player()
        self._create_a_pipe()
        self._create_mouse_pointer()

    def _create_mouse_pointer(self):
        self.mouse = mouse.MousePointer(self.sprites)
        self.sprites.add(self.mouse)

    def _create_player(self):
        p = player.Player(300, 102, self.map)
        self.sprites.add(p)

    def _create_a_pipe(self):
        p = pipe.Pipe(1, 603, 478, self.map)
        self.sprites.add(p)

        p = pipe.Pipe(1, 200, 300, self.map)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            self.mouse.on_click(x, y)
