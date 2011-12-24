# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pygame
import scene
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

class Texto(pygame.sprite.Sprite):

    def __init__(self, font, texto, y):
        self.font = font
        pygame.sprite.Sprite.__init__(self)

        imagen = self._create_text_image(texto)
        self.image = imagen
        self.rect = imagen.get_rect()
        self.z = -50
        self.rect.y = y
        self.rect.centerx = 1200 / 2

    def _create_text_image(self, text):
        white = (255, 255 ,255)
        return self.font.render(text, 1, white)

class Cursor(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = common.load("cursor.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = 1200 / 2

    def definir_posicion(self, posicion):
        self.rect.y = posicion + 10

class Menu(scene.Scene):

    def __init__(self, world, nivel=1):
        scene.Scene.__init__(self, world)
        self.sprites = group.Group()
        self.font = pygame.font.Font("data/FreeSans.ttf", 65)
        self._draw_background()
        self.cursor = Cursor()
        self.cursor.definir_posicion(self.obtener_posicion(0))
        self.sprites.add(self.cursor)

        self._crear_textos()

        self.mouse = editor_mouse.EditorMouse()
        self.sprites.add(self.mouse)

    def poner_el_mouse_por_arriba(self):
        self.sprites.remove(self.mouse)
        self.sprites.add(self.mouse)

    def _crear_textos(self):
        textos = ["comenzar a jugar", "editar niveles", u"ver presentación", "salir"]

        for (indice, texto) in enumerate(textos):
            self.sprites.add(Texto(self.font, texto, self.obtener_posicion(indice)))
            
    def obtener_posicion(self, indice):
        return 350 + indice * 100

    def obtener_indice_para_esta_posicion(self, posicion_vertical):
        return (posicion_vertical - 350) / 100


    def update(self):
        self.mouse.update()

    def draw(self, screen):
        self.sprites.clear(screen, self.background)
        pygame.display.update(self.sprites.draw(screen))

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.world.change_scene(presents.Presents(self.world))
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            indice = self.obtener_indice_para_esta_posicion(y)

            if 0 <= indice < 4:
                self.cursor.definir_posicion(self.obtener_posicion(indice))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            indice = self.obtener_indice_para_esta_posicion(y)

            if indice == 0:
                self.world.change_scene(game.Game(self.world))
            elif indice == 1:
                self.world.change_scene(editor.Editor(self.world))
            elif indice == 2:
                self.world.change_scene(presents.Presents(self.world))
            elif indice == 3:
                import sys
                sys.exit(0)
                

    def _draw_background(self):
        "Imprime y actualiza el fondo de pantalla para usar dirtyrectagles mas adelante."
        self.background = common.load("background_menu.jpg", False)
        #self.map.draw_over(self.background)
        self.world.screen.blit(self.background, (0, 0))

        # actualiza toda la pantalla.
        pygame.display.flip()

    def avisar(self, texto):
        sprite = Texto(self.font, texto)
        self.sprites.add(sprite)

        if self.ultimo_avisar:
            self.ultimo_avisar.kill()
            self.sprites.remove(self.ultimo_avisar)

        self.ultimo_avisar = sprite

    def probar_nivel(self):
        import game
        self.world.change_scene(game.Game(self.world, level=self.mapa.numero, modo_editor=True))

    def avanzar(self):
        self.world.change_scene(Editor(self.world, self.nivel + 1))

    def retroceder(self):
        if self.nivel > 1:
            self.world.change_scene(Editor(self.world, self.nivel - 1))

