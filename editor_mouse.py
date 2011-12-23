# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pygame
import sys
from sprite import Sprite
import common

class EditorMouse(Sprite):
    """Representa el puntero del mouse que interactua con los
    sprites del juego.

    El mouse conoce los objetos de la escena y utiliza estrategias
    para representar cada uno de los estados: Normal, Dragged y Drop
    (ver mouse_state.py).
    """

    def __init__(self, stage_objects=[]):
        Sprite.__init__(self)
        pygame.mouse.set_visible(False)
        self._load_frames()
        self.show()
        self.set_frame('normal')
        self.rect = self.image.get_rect()
        self.stage_objects = stage_objects
        self.z = -50

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

    def on_click(self, x, y):
        self.state.on_click(x, y)

    def hide(self):
        "Oculta temporalmente el puntero del mouse."
        self.visible = False
        self.set_frame("hide")

    def show(self):
        "Mostrando el puntero del mouse."
        self.visible = True
        self.set_frame("normal")
