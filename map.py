# -*- coding: utf-8 -*-
import pygame
import common
import placeholder

class Map:
    "Representa todo el escenario, donde pisar, donde no..."

    def __init__(self, sprites):
        self._create_map()
        self._load_images()
        self.sprites = sprites

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
                self._draw_tile_over(surface, index, r, c)

    def _draw_tile_over(self, surface, tile_number, row, col):
        "Imprime un bloque sobre la superficie indicada por argumento."
        if tile_number != ' ' and tile_number != '\n':
            if tile_number == '_':
                self._create_placeholder(col, row)
            else:
                surface.blit(self.images[tile_number], (col * 75, row * 75))
        
    def _create_placeholder(self, col, row):
        x = col * 75
        y = row * 75
        
        p = placeholder.Placeholder(x, y)
        self.sprites.add(p)

    def can_stand_here(self, x, y):
        "Indica si sobre una coordenada hay un bloque ocupado con suelo."
        row = y / 75
        col = x / 75
        return not self.map[row][col].isspace()
