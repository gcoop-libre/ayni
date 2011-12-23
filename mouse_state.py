# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import pygame
import player
import pipe
import placeholder


class MouseState:
    "Es un estado de comportamiento del mouse."

    def __init__(self, mouse):
        self.mouse = mouse
        # muestra el estado del mouse en la ventana.
        #pygame.display.set_caption(str(self))

    def update(self):
        pass

    def on_click(self, x, y):
        pass

    def select_player(self, player):
        # Si hay un personaje seleccionado lo deselecciona
        if self.mouse.selected_player:
            self.mouse.selected_player.is_not_selected()

        self.mouse.selected_player = player
        self.mouse.selected_player.is_selected()

        # dependiendo de si tiene pieza o no...
        if player.has_a_pipe_in_hands:
            self.mouse.change_state(PointToWorkAt(self.mouse, player))
        else:
            self.mouse.change_state(PointAt(self.mouse, player))


class PointToWorkAt(MouseState):
    """Está por indicarle una coordenada a un trabajador que tiene una pieza.

    En este estado pueden pasar:

        * 1 - que el usuario le indice un placeholder vacio (mejor de los casos).
        * 2 - que le indique un lugar cualquiera para caminar.
        * 3 - que seleccione otro personaje.
        * 4 - que indique el suelo para dejar la pieza.
    """

    def __init__(self, mouse, player):
        MouseState.__init__(self, mouse)
        self.player = player
        self.mouse.set_frame("normal")

    def update(self):
        sprite = self.mouse.get_placeholder_over_mouse()
        player = self.mouse.get_player_over_mouse()

        if sprite or player:
            self.mouse.set_frame("over")
        else:
            self.mouse.set_frame("normal")

        # BUGFIX: cambia el estado del mouse si el personaje logro tomar una pieza.
        if not self.player.has_a_pipe_in_hands:
            self.select_player(self.player)
            #print "BUGFIX!!! el personaje NOOOOOOOO tiene un pipe."
            return


    def on_click(self, x, y):
        placeholder = self.mouse.get_placeholder_over_mouse()
        player = self.mouse.get_player_over_mouse()


        # Caso 1: se le indica un placeholder vacio
        if placeholder and self.player.can_receive_new_jobs():
            pipe = self.player.state.pipe
            self.player.walk_and_work_in_a_placeholder(pipe, placeholder, x, y)
            return

        # Caso 2: se le indica un lugar cualquiera para caminar
        if not player and self.player.can_receive_new_jobs():
            self.player.walk_to_with_piece(self.player.state.pipe, x, y)
            return

        # Caso 3: selecciono otro personaje distinto
        if player and player is not self.player:
            self.select_player(player)

        # Caso 4: Intenta dejar la pieza.
        if self.player.has_a_pipe_in_hands:
            dist = abs(y - self.player.rect.bottom)

            if dist < 26:
                self.player.walk_to_leave_pipe_here(self.player.state.pipe, x, y)

class PointAt(MouseState):
    """Está por indicarle una coordenada a un trabajador que no tiene pieza.

    En este estado puede pasar:

        * 1 - otro jugador.
        * 2 - una pieza.
        * 3 - cualquier lugar para caminar.
    """

    def __init__(self, mouse, player):
        MouseState.__init__(self, mouse)
        self.player = player
        self.mouse.set_frame("normal")

    def update(self):
        sprite = self.mouse.get_pipe_over_mouse()
        player = self.mouse.get_player_over_mouse()

        if sprite or player:
            self.mouse.set_frame("over")
        else:
            self.mouse.set_frame("normal")

        # BUGFIX: cambia el estado del mouse si el personaje logro tomar una pieza.
        if self.player.has_a_pipe_in_hands:
            self.select_player(self.player)
            #print "BUGFIX!!! el personaje tiene un pipe."
            return

    def on_click(self, x, y):
        pipe = self.mouse.get_pipe_over_mouse()
        player = self.mouse.get_player_over_mouse()


        # caso 1: Si selecciona un personaje distinto cambia.
        if player and player is not self.player:
            self.select_player(player)
            return

        # caso 2: Si selecciona una pieza trata de tomarla.
        if pipe and self.player.can_receive_new_jobs():
            if pipe.are_in_a_placeholder:
                placeholder = pipe.get_placeholder()
                self.player.walk_to_remove_a_pipe_from_placeholder(pipe, placeholder, x, y)
            else:
                self.player.walk_and_take_the_pipe(pipe, x, y)

            return

        
        # caso 3:
        if not pipe and not player and self.player.can_receive_new_jobs():
            self.player.walk_to(x, y)

            
class Normal(MouseState):
    "Representa el mouse cuando explora la escena y no ha pulsado."

    def __init__(self, mouse):
        MouseState.__init__(self, mouse)
        self.mouse.set_frame("normal")

    def update(self):
        if self.mouse.visible:
            sprite = self.mouse.get_player_over_mouse()

            if sprite and sprite.can_receive_new_jobs():
                self.mouse.set_frame("over")
            else:
                self.mouse.set_frame("normal")

    def on_click(self, x, y):
        new_sprite = self.mouse.get_player_over_mouse()

        # si no esta trabajando en este momento...
        if new_sprite and new_sprite.can_receive_new_jobs():
            self.select_player(new_sprite)
