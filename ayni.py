# -*- encoding: utf-8 -*-
import world
import game

def run():
    "Genera el objeto World y le asigna una escena."

    w = world.World()
    new_scene = game.Game(w)
    w.change_scene(new_scene)
    w.loop()
