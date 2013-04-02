#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import world
import game
import title
import intro
import presents
import editor
import end
import demo_game
import menu
import config

def run():
    "Genera el objeto World y le asigna una escena."

    w = world.World()
    if config.DISABLE_INTRO:
        new_scene = menu.Menu(w)
    else:
        new_scene = presents.Presents(w)

    #new_scene = game.Game(w)
    #new_scene = demo_game.DemoGame(w)
    #new_scene = end.End(w)
    #new_scene = editor.Editor(w)
    #new_scene = menu.Menu(w)

    w.change_scene(new_scene)
    w.loop()

def run_in_sugar():
    w = world.World(in_sugar_olpc=True)
    new_scene = intro.Intro1(w)
    w.change_scene(new_scene)
    w.loop()

if __name__ == "__main__":
    run()
