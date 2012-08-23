# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import pygame
import random
import sys
import animation

Sprite = pygame.sprite.Sprite


ENABLE_SOUND = False


class Audio:
    "Representa el sistema de sonidos."

    def __init__(self):
        if ENABLE_SOUND:
            self.dialogs = [
                    pygame.mixer.Sound('sounds/aimda2.wav'),
                    pygame.mixer.Sound('sounds/naram2.wav'),
                    pygame.mixer.Sound('sounds/riqs2.wav'),
                    ]

    def player_say(self):
        if ENABLE_SOUND:
            sound = random.choice(self.dialogs)
            sound.play()


class Sprite(pygame.sprite.Sprite):
    "Representa un objeto del juego que se puede apuntar y seleccionar."

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def on_click(self, x, y):
        pass

    def can_click_it(self, x, y):
        return self.rect.collidepoint(x, y)


class Item(Sprite):

    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = load("bridge_item.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = x, y


class Bridge(Sprite):

    def __init__(self, x, y):
        Sprite.__init__(self)
        self._load_animation()
        self.image = self.animation.get_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.creating = False

    def _load_animation(self):
        sheet = animation.Sheet(load("bridge.png", True), 5)
        self.animation = animation.Animation(sheet, 50, [0, 1, 2, 3, 4], True)

    def update(self):
        if self.creating:
            self.update_animation()

    def update_animation(self):
        self.animation.update()
        self.image = self.animation.get_image()

    def on_click(self, x, y):
        if self.rect.collidepoint(x, y):
            if not self.creating:
                self.creating = True


# MOVED
def load(filepath, use_alpha=False):
    "Carga una imagen optimizando la velocidad de impresion."
    image = pygame.image.load("data/" + filepath)

    if use_alpha:
        return image.convert_alpha()
    
    return image.convert()


# MOVED
class MousePointer(Sprite):

    def __init__(self, stage_objects):
        pygame.sprite.Sprite.__init__(self)
        pygame.mouse.set_visible(False)
        self._load_frames()
        self.show()
        self.set_frame('normal')
        self.rect = self.image.get_rect()
        self.stage_objects = stage_objects

    def _load_frames(self):
        self.frames = {
                'normal': load("mouse.png", True),
                'over': load("over.png", True),
                'hide': load("hide.png", True),
                }

    def set_frame(self, name):
        self.image = self.frames[name]

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()

        if self.visible:
            if self.are_over_any_stage_object():
                self.set_frame("over")
            else:
                self.set_frame("normal")

    def are_over_any_stage_object(self):
        x, y = self.rect.topleft
        for sprite in self.stage_objects:
            if sprite.can_click_it(x, y):
                return True

    def hide(self):
        self.visible = False
        self.set_frame("hide")

    def show(self):
        self.visible = True
        self.set_frame("normal")

class Balloon(Sprite):
    "Un globo que tiene texto representando lo que dice un personaje."

    def __init__(self, text_image, x, y):
        Sprite.__init__(self)
        self.image = load('balloon.png', True)
        self.rect = self.image.get_rect()
        self.rect.right = x + 70
        self.rect.bottom = y
        self.time_to_live = 150
        self.image.blit(text_image, (5, 5))

        # Evita que el cuadro de dialogo salga de la pantalla
        if self.rect.left < 2:
            self.rect.left = 2
        elif self.rect.right > 638:
            self.rect.right = 638

    def update(self):
        self.time_to_live -= 1

        if self.time_to_live < 0:
            self.kill()


class Messages:
    "Representa todos los mensajes del juego."

    def __init__(self, sprites):
        self.sprites = sprites
        self.font = pygame.font.Font("data/FreeSans.ttf", 14)
        self.last_sprite = None

    def add(self, text, x, y):
        text_image = self._create_text_image(text)
        new_sprite = Balloon(text_image, x, y)
        self.remove_last_balloon_sprite()
        self.sprites.add(new_sprite)
        self.last_sprite = new_sprite
    
    def remove_last_balloon_sprite(self):
        "Elimina el ultimo mensaje para que no se solapen."

        if self.last_sprite and self.last_sprite.alive():
            self.last_sprite.kill()
            self.last_sprite = None

    def _create_text_image(self, text):
        black = (0, 0, 0)
        return self.font.render(text, 1, black)


# REPLACED en game.py por la clase de pygame.
class Group(pygame.sprite.OrderedUpdates):
    "Representa un contenedor de sprites."

    def __init__(self, *k):
        pygame.sprite.OrderedUpdates.__init__(self, *k)
    
    def on_click(self, x, y):
        "Emite el evento de pulsacion a todos los sprites hijos."
        for s in self:
            s.on_click(x, y)


# MOVED
class Map:
    "Representa todo el escenario, donde pisar, donde no..."

    def __init__(self, sprites, stage_objects):
        self.tile = load('normal.png', True)
        self._create_map()
        self.sprites = sprites
        self.stage_objects = stage_objects
        self._load_images()

    def _create_map(self):
        "Genera la matriz con todos los bloques que se deben imprimir."
        self.map = [
                    '                 ',
                    '788888889  788888',
                    '4       6  4     ',
                    '6       6        ',
                    '6                ',
                    '4                ',
                    '1223  18883      ',
                    '                 ',
                    '                 ',
                    ]

    def _load_images(self):
        "Carga las imagenes de los pipes para pintar."

        self.images = {
            '1': load('pipes/1.png', True),
            '2': load('pipes/2.png', True),
            '3': load('pipes/3.png', True),
            '4': load('pipes/4.png', True),
            '6': load('pipes/6.png', True),
            '7': load('pipes/7.png', True),
            '8': load('pipes/8.png', True),
            '9': load('pipes/9.png', True),
        }

    def draw_over(self, surface):
        "Dibuja el escenario sobre una superficie."

        for r, row in enumerate(self.map):
            for c, index in enumerate(row):
                self._draw_tile_over(surface, index, r, c)

    def _draw_tile_over(self, surface, tile_number, row, col):
        "Imprime un bloque sobre la superficie indicada por argumento."
        if tile_number != ' ':
            surface.blit(self.images[tile_number], (col * 75, row * 75))
        elif tile_number == '\\':
            self.create_bridge(col, row)

    def create_bridge(self, col, row):
        x, y = col * 75 -1, row * 75 + 14
        bridge = Bridge(x, y)
        self.sprites.add(bridge)
        self.stage_objects.add(bridge)

    def can_stand_here(self, x, y):
        "Indica si sobre una coordenada hay un bloque ocupado con suelo."
        row = y / 64
        col = x / 64
        return not self.map[row][col].isspace()


# MOVED
class State:
    "Representa un estado del personaje del juego."

    def __init__(self, player):
        self.player = player
        #print "pasando al estado", self.__class__.__name__

    def on_click(self, x, y):
        pass

    def update(self):
        pass


# MOVED
class Stand(State):
    "El personaje esta en estado 'parado' o 'esperando'"

    def __init__(self, player):
        State.__init__(self, player)
        self.player.set_animation("stand")

    def on_click(self, x, y):
        if self.player.collides(x, y):
            self.player.change_state(Wait(self.player))


# MOVED
class Walk(State):
    "Se mueve a la posición que le indiquen."

    def __init__(self, player, x, y):
        State.__init__(self, player)
        # a 'y' no le da bola...
        self.to_x = x
        self.player.messages.remove_last_balloon_sprite()
        self.player.set_animation("walk")

        if player.rect.centerx < x:
            self.dx = 2
        else:
            self.dx = -2

    def update(self):
        # Verifica obstaculos
        x, y = self.player.rect.centerx + self.dx, self.player.rect.y + 20

        if self.player.can_move_to(x, y):
            if not self._closer():
                self.player.rect.x += self.dx
            else:
                self.player.say("listo...")
                self.player.change_state(Stand(self.player))
        else:
            self.player.change_state(Refuse(self.player))

    def _closer(self):
        "Indica si está muy, muy cerca de el lugar a donde ir."
        return abs(self.player.rect.centerx - self.to_x) < 3


# MOVED
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

# MOVED
class Wait(State):
    "El personaje espera que le digan que hacer."

    def __init__(self, player):
        State.__init__(self, player)
        player.say("Decime...")
        player.set_animation('wait')

    def on_click(self, x, y):
        "Intenta ir al punto indicado o advierte si lo re-seleccionan."

        # Si lo seleccionan de nuevo se queja...
        if self.player.collides(x, y):
            self._repeat_instructions()
            return

        # Va a donde le indiquen.
        if self.player.can_move_to(x, y):
            #self.player.say(u"ahí voy...")
            self.player.change_state(Walk(self.player, x, y))
        else:
            # Si le dicen que se tire, no es boludo...
            self.player.change_state(Refuse(self.player))


    def _repeat_instructions(self):
        "Repite al usuario que le indique el camino."
        messages = [
                u"si, ok, ¿que hago?",
                u"indicame el camino...",
                u"¿a donde?",
                ]
        any_text = random.choice(messages)
        self.player.say(any_text)


# MOVED
class Player(Sprite):
    "Representa un personaje del juego."

    def __init__(self, x, y, messages, map, audio):
        Sprite.__init__(self)
        self._load_frames()
        self.set_animation("stand")
        self.rect = self.image.get_rect()
        self.rect.move_ip((x, y))
        self.messages = messages
        self.audio = audio
        self.say(u"Hola, ¿como andas?")
        self.change_state(Stand(self))
        self.map = map

    def _load_frames(self):
        sheet_walk = animation.Sheet(load("walk.png", True), 4)
        sheet_stand = animation.Sheet(load("stand.png", True), 1)
        sheet_wait = animation.Sheet(load("wait.png", True), 3)
        sheet_boo = animation.Sheet(load("boo.png", True), 1)
        sheet_ok = animation.Sheet(load("ok.png", True), 1)

        self.animations = {
                "walk": animation.Animation(sheet_walk, 5, [0, 1, 2, 3]),
                "stand": animation.Animation(sheet_stand, 1, [0]),
                "boo": animation.Animation(sheet_boo, 1, [0]),
                "ok": animation.Animation(sheet_ok, 1, [0]),
                "wait": animation.Animation(sheet_wait, 10, [0, 1, 2, 1]),
                }

    def set_animation(self, name):
        self.animation = self.animations[name]
        self.image = self.animation.get_image()

    def update(self):
        self.state.update()
        self.animation.update()
        self.image = self.animation.get_image()

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

        # estima si a donde quiere ir hay un piso unos pixels mas abajo...
        return self.map.can_stand_here(x, y + 20)



# MOVED
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Ayni")
pygame.font.init()

if ENABLE_SOUND:
    pygame.mixer.init()

# MOVED
clock = pygame.time.Clock()

sprites = Group()
stage_objects = Group()


messages = Messages(sprites)
map = Map(sprites, stage_objects)
audio = Audio()
player = Player(200, 235, messages, map, audio)


sprites.add(player)
stage_objects.add(player)


# MOVED
background = load("background.jpg", False)

map.draw_over(background)


item = Item(130, 273)
sprites.add(item)
stage_objects.add(item)



screen.blit(background, (0, 0))
pygame.display.flip()

mouse_pointer = MousePointer(stage_objects)
sprites.add(mouse_pointer)

# moved
quit = False

# moved
while not quit:
    sprites.update()
    sprites.clear(screen, background)

    # moved
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            sprites.on_click(x, y)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            elif event.key in [pygame.K_f, pygame.K_F3]:
                pygame.display.toggle_fullscreen()

        if event.type == pygame.ACTIVEEVENT:
            if event.gain:
                mouse_pointer.show()
            else:
                mouse_pointer.hide()

    pygame.display.update(sprites.draw(screen))

    # moved
    clock.tick(60)

sprites.empty()
