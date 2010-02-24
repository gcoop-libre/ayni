# -*- coding: utf-8 -*-
import pygame
import player
import pipe


class MouseState:
    "Es un estado de comportamiento del mouse."

    def __init__(self, mouse):
        self.mouse = mouse

    def update(self):
        pass

    def on_click(self, x, y):
        pass

class PointAt(MouseState):
    "Está por indicarle una coordenada a un trabajador."

    def __init__(self, mouse, player):
        MouseState.__init__(self, mouse)
        self.player = player
        self.mouse.set_frame("normal")

    def update(self):
        pass

    def on_click(self, x, y):
        self.player.walk_to(x, y)
        self.mouse.change_state(Normal(self.mouse))

class Dragging(MouseState):
    "Representa la estrategia del mouse cuando arrastra un objeto."

    def __init__(self, mouse, pipe_to_drag):
        MouseState.__init__(self, mouse)
        self.pipe_to_drag = pipe_to_drag
        self.previous_pipe_position = pygame.Rect(pipe_to_drag.rect)
        self.mouse.set_frame('dragging')

        x, y = self.mouse.rect.topleft 
        px, py = self.pipe_to_drag.rect.topleft

        self.dx = x - px
        self.dy = y - py

    def update(self):
        x, y = self.mouse.rect.topleft 
        self.pipe_to_drag.x = x - self.dx
        self.pipe_to_drag.y = y - self.dy

    def on_click(self, x, y):
        ph = self.mouse.get_placeholder_over_mouse()

        if ph:
            self.pipe_to_drag.x = ph.rect.x
            self.pipe_to_drag.y = ph.rect.y
        else:
            x, y = self.previous_pipe_position.topleft
            self.pipe_to_drag.move_to(x, y)
            #self.pipe_to_drag.rect = self.previous_pipe_position

        self.mouse.change_state(Normal(self.mouse))
            
class Normal(MouseState):
    "Representa el mouse cuando explora la escena y no ha pulsado."

    def __init__(self, mouse):
        MouseState.__init__(self, mouse)
        self.mouse.set_frame("normal")

    def update(self):
        if self.mouse.visible:
            sprite = self.mouse.get_object_over_mouse()

            if sprite:
                self.mouse.set_frame("over")
            else:
                self.mouse.set_frame("normal")

    def on_click(self, x, y):
        sprite = self.mouse.get_object_over_mouse()

        if sprite:
            # Determina el tipo de objeto que es.

            if isinstance(sprite, player.Player):
                self.mouse.change_state(PointAt(self.mouse, sprite))
            elif isinstance(sprite, pipe.Pipe):
                pipe_to_drag = sprite
                self.mouse.change_state(Dragging(self.mouse, pipe_to_drag))
