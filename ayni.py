#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import world
import game

def run():
    "Genera el objeto World y le asigna una escena."

    w = world.World()
    new_scene = game.Game(w)
    w.change_scene(new_scene)
    w.loop()


if __name__ == "__main__":
    run()
