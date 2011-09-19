# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import pygame
import random
import sys
import animation
import common
import mouse_state
import placeholder
import player
import pipe
from sprite import Sprite

class MousePointer(Sprite):
    """Representa el puntero del mouse que interactua con los
    sprites del juego.

    El mouse conoce los objetos de la escena y utiliza estrategias
    para representar cada uno de los estados: Normal, Dragged y Drop
    (ver mouse_state.py).
    """

    def __init__(self, stage_objects):
        Sprite.__init__(self)
        pygame.mouse.set_visible(False)
        self._load_frames()
        self.show()
        self.set_frame('normal')
        self.rect = self.image.get_rect()
        self.stage_objects = stage_objects
        self.change_state(mouse_state.Normal(self))
        self.z = -50
        self.selected_player = None

    def _load_frames(self):
        self.frames = {
                'normal':   common.load("mouse.png", True),
                'over':     common.load("over.png", True),
                'dragging': common.load("dragging.png", True),
                'hide':     common.load("hide.png", True),
                }

    def set_frame(self, name):
        self.image = self.frames[name]

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()
        self.state.update()

    def on_click(self, x, y):
        self.state.on_click(x, y)

    """
    def get_object_over_mouse(self):
        "Retorna cualquier objeto que se encuentre debajo del mouse."
        x, y = self.rect.topleft
        for sprite in self.stage_objects:
            if sprite.can_be_clicked and sprite.collide_with(x, y):
                return sprite
    """
        
    def get_placeholder_over_mouse(self):
        "Retorna el bloque para colocar piezas debajo del cursor."
        x, y = self.rect.topleft
        for sprite in self.stage_objects:
            if isinstance(sprite, placeholder.Placeholder) and sprite.collide_with(x, y):
                return sprite

    def get_player_over_mouse(self):
        "Retorna el bloque para colocar piezas debajo del cursor."
        x, y = self.rect.topleft
        for sprite in self.stage_objects:
            if isinstance(sprite, player.Player) and sprite.collide_with(x, y):
                return sprite

    def get_pipe_over_mouse(self):
        x, y = self.rect.topleft
        for sprite in self.stage_objects:
            if isinstance(sprite, pipe.Pipe) and sprite.collide_with(x, y):
                return sprite

    def hide(self):
        "Oculta temporalmente el puntero del mouse."
        self.visible = False
        self.set_frame("hide")

    def show(self):
        "Mostrando el puntero del mouse."
        self.visible = True
        self.set_frame("normal")

    def change_state(self, state):
        self.state = state
