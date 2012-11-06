# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import pygame
import scene
import config
import common
import mouse
import pipe
import group
import messages
import level_complete
import particles
import end
import presents
import editor_mouse
import game
import editor
import nubes

class Texto(pygame.sprite.Sprite):

    def __init__(self, font, texto, x, y):
        self.font = font
        pygame.sprite.Sprite.__init__(self)

        imagen = self._create_text_image(texto)
        self.image = imagen
        self.rect = imagen.get_rect()
        self.z = -50
        self.rect.y = y
        self.rect.centerx = x

    def _create_text_image(self, text):
        white = (255, 255 ,255)
        black = (0, 0, 0)
        image = self.font.render(text, 1, black)
        image_white = self.font.render(text, 1, white)
        image_black = self.font.render(text, 1, black)
        rect = image_white.get_rect()
        image.blit(image_black, (3, 3))
        image.blit(image_white, (1, 1))
        return image

class Cursor(pygame.sprite.Sprite):

    def __init__(self, world, actions):

        pygame.sprite.Sprite.__init__(self)
        self.image = common.load("cursor.png", True, (int(config.WIDTH * 0.8), int(config.HEIGHT * 0.09)))
        self.rect = self.image.get_rect()
        self.rect.centerx = config.WIDTH / 2
        self.posicion_actual = 0
        self.world = world
        self.actions = actions

    def definir_posicion(self, posicion):
        self.posicion_actual = posicion % 4
        self.rect.y = int(config.HEIGHT * 0.4) + self.posicion_actual * int(config.HEIGHT * 0.1) + int(config.HEIGHT * 0.01)

    def avanzar(self):
        self.definir_posicion(self.posicion_actual + 1)

    def retroceder(self):
        self.definir_posicion(self.posicion_actual -1)

    def seleccionar(self):
        indice = self.posicion_actual
        self.world.change_scene(self.actions[indice][1](self.world))

class Logo(pygame.sprite.Sprite):
    "El texto de indica: 'presents'"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = common.load('title.png', True, (config.WIDTH * 0.3, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = config.WIDTH / 2
        self.rect.y = config.HEIGHT * 0.09

class Menu(scene.Scene):

    def __init__(self, world, nivel=1):
        scene.Scene.__init__(self, world)

        self.items = [
                (u"Comenzar a jugar", game.Game),
                (u"Editar niveles", editor.Editor),
                (u"Ver presentación",presents.Presents),
                (u"Salir", world.salir),
                ]
        if config.DISABLE_EDITOR:
            self.items.pop(1)
        self.sprites = group.Group()
        self.nubes = nubes.Nubes(self.sprites)
        self.font = pygame.font.Font(common.get_ruta('FreeSans.ttf'), int(config.HEIGHT * 0.08))
        self.font_small = pygame.font.Font(common.get_ruta('FreeSans.ttf'), int(config.HEIGHT * 0.04))
        self._draw_background()
        self.cursor = Cursor(world, self.items)
        self.cursor.definir_posicion(0)
        self.sprites.add(self.cursor)

        self._crear_textos()
        self._crear_logotipo()


        self.mouse = editor_mouse.EditorMouse()
        self.sprites.add(self.mouse)

    def _crear_logotipo(self):
        self.logo = Logo()
        self.sprites.add(self.logo)

    def poner_el_mouse_por_arriba(self):
        self.sprites.remove(self.mouse)
        self.sprites.add(self.mouse)

    def _crear_textos(self):

        for (indice, item) in enumerate(self.items):
            self.sprites.add(Texto(self.font, item[0], config.WIDTH/2, self.obtener_posicion(indice)))

        self.sprites.add(Texto(self.font_small, 'version: %s' % config.VERSION, int(config.WIDTH * 0.9), int(config.HEIGHT * 0.9)))

    def obtener_posicion(self, indice):
        return int(config.HEIGHT * 0.4) + indice * int(config.HEIGHT * 0.1)

    def obtener_indice_para_esta_posicion(self, posicion_vertical):
        return (posicion_vertical - int(config.HEIGHT * 0.4)) / int(config.HEIGHT * 0.1)

    def update(self):
        self.mouse.update()
        self.nubes.update()

    def draw(self, screen):
        self.sprites.clear(screen, self.background)
        pygame.display.update(self.sprites.draw(screen))

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.world.change_scene(presents.Presents(self.world))
            elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                self.cursor.seleccionar()
            elif event.key == pygame.K_DOWN:
                self.cursor.avanzar()
            elif event.key == pygame.K_UP:
                self.cursor.retroceder()
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            indice = self.obtener_indice_para_esta_posicion(y)

            if 0 <= indice < 4:
                self.cursor.definir_posicion(indice)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            self.cursor.seleccionar()


    def _draw_background(self):
        "Imprime y actualiza el fondo de pantalla para usar dirtyrectagles mas adelante."
        self.background = common.load("background_menu.jpg", False, (config.WIDTH, config.HEIGHT))
        #self.map.draw_over(self.background)
        self.world.screen.blit(self.background, (0, 0))

        # actualiza toda la pantalla.
        pygame.display.flip()

    def probar_nivel(self):
        import game
        self.world.change_scene(game.Game(self.world, level=self.mapa.numero, modo_editor=True))

    def avanzar(self):
        self.world.change_scene(Editor(self.world, self.nivel + 1))

    def retroceder(self):
        if self.nivel > 1:
            self.world.change_scene(Editor(self.world, self.nivel - 1))

