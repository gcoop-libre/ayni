# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import pygame
import common
import placeholder
import player
import pipe

class Map:
    "Representa todo el escenario, donde pisar, donde no..."

    def __init__(self, sprites):
        self._create_map()
        self._load_images()
        self.sprites = sprites
        self.placeholders = []

    def _create_map(self):
        "Genera la matriz con todos los bloques que se deben imprimir."
        path = 'data/map/1.txt'
        f = open(path, 'rt')
        self.map = f.readlines()
        f.close()

    def _load_images(self):
        "Carga las imagenes de los pipes para pintar."

        self.images = {
            '1': common.load('pipes/1.png', True),
            '2': common.load('pipes/2.png', True),
            '3': common.load('pipes/3.png', True),
            '4': common.load('pipes/4.png', True),
            '6': common.load('pipes/6.png', True),
            '7': common.load('pipes/7.png', True),
            '8': common.load('pipes/8.png', True),
            '9': common.load('pipes/9.png', True),
        }

    def draw_over(self, surface):
        "Dibuja el escenario sobre una superficie."

        for r, row in enumerate(self.map):
            for c, index in enumerate(row):
                if index in "qweasdzxc":
                    self._create_pipe_by_index(index, r, c)
                else:
                    self._draw_tile_over(surface, index, r, c)

    def _draw_tile_over(self, surface, tile_number, row, col):
        "Imprime un bloque sobre la superficie indicada por argumento."
        if tile_number != ' ' and tile_number != '\n':
            if tile_number == '_':
                self._create_placeholder(col, row)
            elif tile_number == 'o':
                self._create_player(col, row)
            else:
                surface.blit(self.images[tile_number], (col * 75, row * 75))
        
    def _create_placeholder(self, col, row):
        "Genera un bloque donde se puede colocar una pieza."
        x = col * 75
        y = row * 75
        
        p = placeholder.Placeholder(x, y)
        self.sprites.add(p)
        self.placeholders.append(p)

    def _create_player(self, col, row):
        # Es el desplazamiento vertical que se necesita
        # para que el trabajador toque el suelo exactamente a 
        # la altura correcta...
        dy = 27

        x = col * 75 + 30
        y = (row + 1) * 75 + dy
        
        p = player.Player(x, y, self)
        self.sprites.add(p)

    def can_stand_here(self, x, y):
        "Indica si sobre una coordenada hay un bloque ocupado con suelo."
        row = y / 75
        col = x / 75
        return self.map[row][col] in ['2', '8'] or self.there_are_a_fill_placeholder(row, col)

    def _create_pipe_by_index(self, index, row, col):
        pieces = {
            'q': 7,
            'w': 8,
            'e': 9,
            'a': 4,
            'd': 6,
            'z': 1,
            'x': 2,
            'c': 3,
            }
        x, y = col * 75 + 40, row * 75 + 101
        t = pieces[index]
        self.sprites.add(pipe.Pipe(t, x, y, self))


    def there_are_a_fill_placeholder(self, row, col):
        "Retorna True si hay un placeholder ocupado en la posición indicada."

        x = col * 75
        y = row * 75

        for p in self.placeholders:
            if p.rect.topleft == (x, y) and p.are_used and p.is_floor:
                return True
