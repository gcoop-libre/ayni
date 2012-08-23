# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


class Scene:
    "Es una escena del juego, toda escena debería heredar de aquí."

    def __init__(self, world):
        self.world = world

    def update(self):
        pass

    def draw(self, screen):
        pass

    def on_event(self, event):
        pass
