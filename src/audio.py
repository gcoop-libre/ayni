#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import pygame
import common

ENABLE_SOUND = True

class Audio:
    "Representa el sistema de sonidos."

    def __init__(self):
        if ENABLE_SOUND:
            pygame.mixer.init(48000)

            self.sounds = {
                'working': pygame.mixer.Sound(common.get_ruta(os.path.join('sounds', 'hammer.ogg'))),
                'menu': pygame.mixer.Sound(common.get_ruta(os.path.join('sounds', 'menu.wav'))),
                'click': pygame.mixer.Sound(common.get_ruta(os.path.join('sounds', 'click.wav'))),
                }

    def play(self, name):
        if ENABLE_SOUND:
            self.sounds[name].play()
