# -*- coding: utf-8 -*-
import pygame

class Sprite(pygame.sprite.Sprite):
    """Clase abstracta para representar todos los sprites del juego.

    En general hay dos tipos de sprites, los que se pueden seleccionar
    con el mouse deben tener su atributo ``can_be_clicked`` en True. En
    cambio lo que no se puedan seleccionar (como el propio puntero del
    mouse o decoraciones) tienen que tener este atributo en False."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.can_be_clicked = False

    def collide_with(self, x, y):
        return self.rect.collidepoint(x, y)
