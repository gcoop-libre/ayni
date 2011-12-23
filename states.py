# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# tiempo que tiene que trabajar
TIME_TO_WORK = 40

class State:
    "Representa un estado del personaje del juego."

    def __init__(self, player):
        self.player = player
        #print "PLAYER", self

    def update(self):
        pass


class Stand(State):
    "El personaje esta en estado 'parado' o 'esperando'"

    def __init__(self, player):
        State.__init__(self, player)
        self.player.set_animation("stand")


class StandWithPiece(State):
    "El personaje esta en estado 'parado' o 'esperando' con una pieza."

    def __init__(self, player, pipe):
        self.pipe = pipe
        State.__init__(self, player)
        self.player.set_animation("stand_moving")


class WalkWithPiece(State):
    "Se mueve a la posición que le indiquen."

    def __init__(self, player, pipe, x, y):
        State.__init__(self, player)
        self.pipe = pipe
        self.to_x = x
        self.player.set_animation("walk_moving")

        if player.rect.centerx < x:
            self.dx = 3
            self.player.flip = True
        else:
            self.dx = -3
            self.player.flip = False

    def update(self):
        # Verifica obstaculos
        x, y = self.player.rect.centerx + self.dx, self.player.rect.bottom

        if self.player.can_move_to(x, y):
            if not self._closer():
                self.pipe.x += self.dx
                self.player.rect.x += self.dx
            else:
                self.player.attack_to(self.pipe)
        else:
            self.player.change_state(StandWithPiece(self.player, self.pipe))

    def _closer(self):
        "Indica si está muy, muy cerca de el lugar a donde ir."
        return abs(self.player.rect.centerx - self.to_x) < 3

class WalkToRemoveAPipe(State):
    "Camina hacia un placeholder para quitar la pieza que tenga colocada."

    def __init__(self, player, pipe, placeholder, x, y):
        State.__init__(self, player)
        self.pipe = pipe
        self.placeholder = placeholder
        self.to_x = x
        self.player.set_animation("walk")

        if player.rect.centerx < x:
            self.dx = 3
            self.player.flip = True
        else:
            self.dx = -3
            self.player.flip = False

    def update(self):
        # Verifica obstaculos
        x, y = self.player.rect.centerx + self.dx, self.player.rect.bottom

        if self.player.can_move_to(x, y):
            if not self._closer():
                self.player.rect.x += self.dx
            else:
                if self.player.can_work_on_this_placeholder(self.placeholder):
                    self.player.change_state(WorkToRemovePipeFromPlaceholder(self.player, self.pipe, self.placeholder))
                else:
                    #self.player.say("Estoy muy lejos de ese placeholder...")
                    self.player.change_state(Stand(self.player))
        else:
            if self._closer():
                self.player.change_state(StandWithPiece(self.player, self.pipe))
            else:
                #self.player.say("Estoy muy lejos de ese placeholder...")
                self.player.change_state(Stand(self.player))

    def _closer(self):
        "Indica si está muy, muy cerca de el lugar a donde ir."
        return abs(self.player.rect.centerx - self.to_x) < 3


class WalkWithPieceToLeave(State):
    "Se mueve a la posición que le indiquen."

    def __init__(self, player, pipe, x, y):
        State.__init__(self, player)
        self.pipe = pipe
        self.to_x = x
        self.player.set_animation("walk_moving")

        if player.rect.centerx < x:
            self.dx = 3
            self.player.flip = True
        else:
            self.dx = -3
            self.player.flip = False

    def update(self):
        # Verifica obstaculos
        x, y = self.player.rect.centerx + self.dx, self.player.rect.bottom

        if self.player.can_move_to(x, y):
            if not self._closer():
                self.pipe.x += self.dx
                self.player.rect.x += self.dx
            else:
                self.player.change_state(LeavePipe(self.player, self.pipe))
        else:
                self.player.change_state(StandWithPiece(self.player, self.pipe))


    def _closer(self):
        "Indica si está muy, muy cerca de el lugar a donde ir."
        return abs(self.player.rect.centerx - self.to_x) < 3

class WalkWithPieceToWorkAt(State):
    "Se mueve a la posición que le indiquen."

    def __init__(self, player, pipe, placeholder, x, y):
        State.__init__(self, player)
        self.pipe = pipe
        self.placeholder = placeholder
        self.to_x = x
        self.player.set_animation("walk_moving")

        if player.rect.centerx < x:
            self.dx = 3
            self.player.flip = True
        else:
            self.dx = -3
            self.player.flip = False

    def update(self):
        # Verifica obstaculos
        x, y = self.player.rect.centerx + self.dx, self.player.rect.bottom

        if self.player.can_move_to(x, y):
            if not self._closer():
                self.pipe.x += self.dx
                self.player.rect.x += self.dx
            else:
                if self.player.can_work_on_this_placeholder(self.placeholder):
                    if self.placeholder.are_used:
                        #print "Este placeholder esta en uso."
                        self.player.say("Solo una pieza...")
                        self.player.change_state(StandWithPiece(self.player, self.pipe))
                    else:
                        self.player.change_state(WorkToPutPipe(self.player, self.pipe, self.placeholder))
                else:
                    print "Estoy muy lejos de ese placeholder..."
                    self.player.change_state(StandWithPiece(self.player, self.pipe))
        else:
            self.player.change_state(StandWithPiece(self.player, self.pipe))

    def _closer(self):
        "Indica si está muy, muy cerca de el lugar a donde ir."
        return abs(self.player.rect.centerx - self.to_x) < 3


class WorkToRemovePipeFromPlaceholder(State):
    "Se mueve a la posición que le indiquen."

    def __init__(self, player, pipe, placeholder):
        State.__init__(self, player)
        self.pipe = pipe
        self.placeholder = placeholder
        self.player.set_animation("working")
        self.time_to_leave = TIME_TO_WORK
        player.audio.play('working')
        player.game.create_working_particles_effect(placeholder.rect)

        if placeholder.rect.centerx < player.rect.centerx:
            player.flip = False
        else:
            player.flip = True


    def update(self):
        self.time_to_leave -= 1

        if self.time_to_leave < 0:
            "Quita la pieza de su placeholder y se la da al obrero."
            self.pipe.remove_from_a_placeholder()
            self.player.attack_to(self.pipe)
            # el metodo anterior cambia el estado del player a StandWithPiece

class WorkToPutPipe(State):
    "Se mueve a la posición que le indiquen."

    def __init__(self, player, pipe, placeholder):
        State.__init__(self, player)
        self.pipe = pipe
        self.placeholder = placeholder
        self.player.set_animation("working")
        self.player.has_a_pipe_in_hands = False
        self.pipe.put_in_this_placeholder(placeholder)
        self.time_to_leave = TIME_TO_WORK
        player.audio.play('working')
        player.game.create_working_particles_effect(placeholder.rect)

        if placeholder.rect.centerx < player.rect.centerx:
            player.flip = False
        else:
            player.flip = True


    def update(self):
        self.time_to_leave -= 1

        if self.time_to_leave < 0:
            if self.pipe.is_in_a_right_placeholder():
                self.player.change_state(Ok(self.player))
            else:
                self.player.change_state(Stand(self.player))

class WalkAndTake(State):
    "Se mueve a la posición que le indiquen."

    def __init__(self, player, pipe, x, y):
        State.__init__(self, player)
        self.pipe = pipe
        # a 'y' no le da bola...
        self.to_x = x
        #self.player.messages.remove_last_balloon_sprite()
        self.player.set_animation("walk")

        if player.rect.centerx < x:
            self.dx = 3
            self.player.flip = True
        else:
            self.dx = -3
            self.player.flip = False

    def update(self):
        # Verifica obstaculos
        x, y = self.player.rect.centerx + self.dx, self.player.rect.bottom

        if self.player.can_move_to(x, y):
            if not self._closer():
                self.player.rect.x += self.dx
            else:
                if self.player.can_take_this_piece(self.pipe):
                    self.player.attack_to(self.pipe)
                else:
                    print "No puedo tomar esa pieza, esta un poco lejos..."
                    self.player.change_state(Stand(self.player))

        else:
            self.player.change_state(Stand(self.player))

    def _closer(self):
        "Indica si está muy, muy cerca de el lugar a donde ir."
        return abs(self.player.rect.centerx - self.to_x) < 3


class Walk(State):
    "Se mueve a la posición que le indiquen."

    def __init__(self, player, x, y):
        State.__init__(self, player)
        # a 'y' no le da bola...
        self.to_x = x
        #self.player.messages.remove_last_balloon_sprite()
        self.player.set_animation("walk")

        if player.rect.centerx < x:
            self.dx = 3
            self.player.flip = True
        else:
            self.dx = -3
            self.player.flip = False

    def update(self):
        # Verifica obstaculos
        x, y = self.player.rect.centerx + self.dx, self.player.rect.bottom

        if self.player.can_move_to(x, y):
    
            if not self._closer():
                self.player.rect.x += self.dx
            else:
                self.player.change_state(Stand(self.player))
        else:
            self.player.change_state(Stand(self.player))
            #self.player.say("")

    def _closer(self):
        "Indica si está muy, muy cerca de el lugar a donde ir."
        return abs(self.player.rect.centerx - self.to_x) < 3


"""
class Refuse(State):
    "Aguarda unos instantes y regresa al estado Stand."

    def __init__(self, player):
        State.__init__(self, player)
        self.player.set_animation('boo')
        self.delay = 50
        self.player.say(u"nah, no voy ahí.")

    def update(self):
        self.delay -= 1

        if self.delay < 0:
            self.player.change_state(Stand(self.player))
"""

class LeavePipe(State):
    "Deja la pieza cerca del suelo en donde se encuentra."

    def __init__(self, player, pipe):
        State.__init__(self, player)
        self.player.leave_pipe(pipe)

    def update(self):
        self.player.change_state(Stand(self.player))


class Ok(State):
    "Muestra la aprobación del personaje."

    def __init__(self, player):
        State.__init__(self, player)
        self.player.set_animation("ok")
        self.time_to_leave = TIME_TO_WORK
        self.last_flip_state = player.flip
        player.flip = False

    def update(self):
        self.time_to_leave -= 1

        if self.time_to_leave < 0:
            self.player.flip = self.last_flip_state
            self.player.change_state(Stand(self.player))
            self.player.game.on_pipe_put()

class OkPermanent(State):
    "Muestra la aprobación del personaje cuando termina el nivel."

    def __init__(self, player):
        State.__init__(self, player)
        self.player.set_animation("ok")
        self.last_flip_state = player.flip
        player.flip = False

    def update(self):
        pass
