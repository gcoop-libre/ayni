# -*- coding: utf-8 -*-


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
