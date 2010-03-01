# -*- coding: utf-8 -*-
import pygame
import random
import sys
import animation
import common
from states import *
from sprite import Sprite


class Player(Sprite):
    "Representa un personaje del juego."

    def __init__(self, x, y, map):
        Sprite.__init__(self)
        self._load_frames()
        self.set_animation("stand")
        self.rect = self.image.get_rect()
        self.rect.move_ip((x - self.rect.w / 2, y - self.rect.h))
        #self.messages = messages
        #self.audio = audio
        #self.say(u"Hola, ¿como andas?")
        #self.change_state(Walk(self, 100, 100))
        self.change_state(Stand(self))
        self.map = map
        self.can_be_clicked = True
        self.flip = False
        self.has_a_pipe_in_hands = False

    def _load_frames(self):
        sheet_walk = animation.Sheet(common.load("player/walk.png", True), 4)
        sheet_stand = animation.Sheet(common.load("player/stand.png", True), 1)
        sheet_wait = animation.Sheet(common.load("player/wait.png", True), 2)
        sheet_working = animation.Sheet(common.load("player/working.png", True), 2)
        sheet_ok = animation.Sheet(common.load("player/ok.png", True), 1)
        sheet_stand_moving = animation.Sheet(common.load("player/stand_moving.png", True), 1)
        sheet_walk_moving = animation.Sheet(common.load("player/walk_moving.png", True), 4)

        self.animations = {
                "walk": animation.Animation(sheet_walk, 6, [0, 1, 2, 3]),
                "stand": animation.Animation(sheet_stand, 1, [0]),
                "working": animation.Animation(sheet_working, 6, [0, 1]),
                "ok": animation.Animation(sheet_ok, 1, [0]),
                "wait": animation.Animation(sheet_wait, 10, [0, 1]),
                "stand_moving": animation.Animation(sheet_stand_moving, 1, [0]),
                "walk_moving": animation.Animation(sheet_walk_moving, 6, [0, 1, 2, 3]),
            }

    def set_animation(self, name):
        self.animation = self.animations[name]
        self.image = self.animation.get_image()

    def update(self):
        self.state.update()
        self.animation.update()
        self.image = self.animation.get_image(self.flip)

    def on_click(self, x, y):
        self.state.on_click(x, y)

    def say(self, text):
        x, y = self.rect.topleft
        self.messages.add(text, x, y)
        self.audio.player_say()

    def change_state(self, state):
        self.state = state

    def collides(self, x, y):
        "informa si colisiona con un punto (generalmente el mouse)."
        return self.rect.collidepoint(x, y)

    def can_move_to(self, x, y):
        "Consulta si puede ir a la posicion indicada."
        return self.map.can_stand_here(x, y)

    def walk_to(self, x, y):
        self.change_state(Walk(self, x, y))

    def walk_to_with_piece(self, pipe, x, y):
        self.change_state(WalkWithPiece(self, pipe, x, y))

    def walk_and_take_the_pipe(self, pipe, x, y):
        self.change_state(WalkAndTake(self, pipe, x, y))

    def walk_and_work_in_a_placeholder(self, pipe, placeholder, x, y):
        if self.rect.centerx < x:
            x -= 75
        else:
            x += 75

        self.change_state(WalkWithPieceToWorkAt(self, pipe, placeholder, x, y))

    def walk_to_remove_a_pipe_from_placeholder(self, pipe, placeholder, x, y):
        if self.rect.centerx < x:
            x -= 75
        else:
            x += 75

        self.change_state(WalkToRemoveAPipe(self, pipe, placeholder, x, y))

    def attack_to(self, pipe):
        pipe.y = self.rect.y - 25
        pipe.x = self.rect.x
        self.has_a_pipe_in_hands = True
        self.change_state(StandWithPiece(self, pipe))

    def can_take_this_piece(self, piece):
        "Retorna True si la pieza a tomar está cerca del trabajador."
        return self.are_closer_to(piece)

    def are_closer_to(self, sprite):
        "Informa si el trabajador está cerca de un sprite particular."
        dx = abs(sprite.rect.centerx - self.rect.centerx)
        dy = abs(sprite.rect.centery - self.rect.centery)

        return dx < 180 and dy < 75

    def can_work_on_this_placeholder(self, placeholder):
        "Indica si el trabajador está cerca de un placeholder para colocar una pieza."
        return self.are_closer_to(placeholder)
