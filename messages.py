# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import pygame
from balloon import Balloon

class Messages:
    "Representa todos los mensajes del juego."

    def __init__(self, sprites):
        self.sprites = sprites
        self.font = pygame.font.Font("data/FreeSans.ttf", 14)
        self.last_sprite = None

    def add(self, text, x, y):
        text_image = self._create_text_image(text)
        new_sprite = Balloon(text_image, x, y)
        self.remove_last_balloon_sprite()
        self.sprites.add(new_sprite)
        self.last_sprite = new_sprite
    
    def remove_last_balloon_sprite(self):
        "Elimina el ultimo mensaje para que no se solapen."

        if self.last_sprite and self.last_sprite.alive():
            self.last_sprite.kill()
            self.last_sprite = None

    def _create_text_image(self, text):
        black = (0, 0, 0)
        return self.font.render(text, 1, black)
