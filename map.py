# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import os.path
import pygame
import config
import common
import placeholder
import player
import pipe

class Map:
    "Representa todo el escenario, donde pisar, donde no..."

    def __init__(self, game, sprites, messages, audio, level=2):
        self.pipes = []
        self.players = []
        self._create_map(level)
        self._load_images()
        self.sprites = sprites
        self.placeholders = []
        self.messages = messages
        self.audio = audio
        self.game = game

    def _create_map(self, level=1):
        "Genera la matriz con todos los bloques que se deben imprimir."
        path = common.get_level_file(level)
        f = open(path, 'rt')
        self.map = f.readlines()
        f.close()

    def _load_images(self):
        "Carga las imagenes de los pipes para pintar."

        self.images = {
            '1': common.load('pipes/1.png', True, (config.BLOCK_SIZE, config.BLOCK_SIZE)),
            '2': common.load('pipes/2.png', True, (config.BLOCK_SIZE, config.BLOCK_SIZE)),
            '3': common.load('pipes/3.png', True, (config.BLOCK_SIZE, config.BLOCK_SIZE)),
            '4': common.load('pipes/4.png', True, (config.BLOCK_SIZE, config.BLOCK_SIZE)),
            '6': common.load('pipes/6.png', True, (config.BLOCK_SIZE, config.BLOCK_SIZE)),
            '7': common.load('pipes/7.png', True, (config.BLOCK_SIZE, config.BLOCK_SIZE)),
            '8': common.load('pipes/8.png', True, (config.BLOCK_SIZE, config.BLOCK_SIZE)),
            '9': common.load('pipes/9.png', True, (config.BLOCK_SIZE, config.BLOCK_SIZE)),
        }

    def draw_over(self, surface):
        "Dibuja el escenario sobre una superficie."

#        self.draw_backlayer(surface)

        for r, row in enumerate(self.map):
            for c, index in enumerate(row):
                if index in "qweasdzxc":
                    self._create_pipe_by_index(index, r, c)
                else:
                    self._draw_tile_over(surface, index, r, c)

    def draw_backlayer(self, surface):
        backlayer = common.load('backlayers/1.png', True, (config.WIDTH, config.HEIGHT))
        surface.blit(backlayer, (0, 0))

    def _draw_tile_over(self, surface, tile_number, row, col):
        "Imprime un bloque sobre la superficie indicada por argumento."
        if tile_number != ' ' and tile_number != '\n':
            if tile_number in "rtyfhvbn":
                self._create_placeholder(tile_number, col, row)
            elif tile_number == 'o':
                self._create_player(col, row)
            else:
                surface.blit(self.images[tile_number], (col * config.BLOCK_SIZE, row * config.BLOCK_SIZE))
        
    def _create_placeholder(self, tilenumber, col, row):
        "Genera un bloque donde se puede colocar una pieza."
        x = col * config.BLOCK_SIZE 
        y = row * config.BLOCK_SIZE 

        targets = {
                'r': 7,
                't': 8,
                'y': 9,
                'f': 4,
                'h': 6,
                'v': 1,
                'b': 2,
                'n': 3,
                }

        type = targets[tilenumber]
        
        p = placeholder.Placeholder(type, x, y)
        self.sprites.add(p)
        self.placeholders.append(p)

    def _create_player(self, col, row):
        # Es el desplazamiento vertical que se necesita
        # para que el trabajador toque el suelo exactamente a 
        # la altura correcta...
        dy = int(config.BLOCK_SIZE * 0.36)

        x = col * config.BLOCK_SIZE + int(config.BLOCK_SIZE * 0.4)
        y = (row + 1) * config.BLOCK_SIZE + dy
        
        p = player.Player(self.game, self.audio, self.messages, x, y, self)
        self.sprites.add(p)
        self.players.append(p)

    def can_stand_here(self, x, y):
        "Indica si sobre una coordenada hay un bloque ocupado con suelo."
        row = y / config.BLOCK_SIZE
        col = x / config.BLOCK_SIZE
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
        x, y = col * config.BLOCK_SIZE + int(config.BLOCK_SIZE * 0.53), row * config.BLOCK_SIZE + int(config.BLOCK_SIZE * 1.35)
        t = pieces[index]
        new_pipe = pipe.Pipe(self.game, t, x, y, self)
        self.sprites.add(new_pipe)
        self.pipes.append(new_pipe)


    def there_are_a_fill_placeholder(self, row, col):
        "Retorna True si hay un placeholder ocupado en la posición indicada."

        x = col * config.BLOCK_SIZE 
        y = row * config.BLOCK_SIZE 

        for p in self.placeholders:
            if p.rect.topleft == (x, y) and p.are_used and p.is_floor:
                return True

    def all_pipes_are_in_correct_placeholders(self):
        all_pipes = True

        for x in self.pipes:
            if x.are_in_a_placeholder and x.is_in_a_right_placeholder():
                #print x, "esta correctamente colocada"
                pass
            else:
                if config.DEBUG:
                    print x, "no esta en el placeholder que le corresponde"
                all_pipes = False

        return all_pipes

