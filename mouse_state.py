# -*- coding: utf-8 -*-
import pygame


class MouseState:

    def __init__(self, mouse):
        self.mouse = mouse


class Normal(MouseState):

    def __init__(self, mouse):
        MouseState.__init__(self, mouse)
