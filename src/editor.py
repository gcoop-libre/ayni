# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pygame
import scene
import config
import common
import map
import mouse
import pipe
import group
import messages
import level_complete
import particles
import end
import editor_mouse
import menu
import os

def cargar_imagen_por_codigo(codigo):
    referencias = {
        'o': "player/ico.png",
        '1': "pipes/1.png",
        '2': "pipes/2.png",
        '3': "pipes/3.png",
        '4': "pipes/4.png",
        '6': "pipes/6.png",
        '7': "pipes/7.png",
        '8': "pipes/8.png",
        '9': "pipes/9.png",
        'v': "pipes/v.png",
        't': "pipes/t.png",
        'n': "pipes/n.png",
        'f': "pipes/f.png",
        'r': "pipes/r.png",
        'y': "pipes/y.png",
        'z': "front_pipes/1.png",
        'x': "front_pipes/2.png",
        'c': "front_pipes/3.png",
        'a': "front_pipes/4.png",
        'q': "front_pipes/7.png",
        'e': "front_pipes/9.png",
    }

    return common.load(referencias[codigo], True, (config.BLOCK_SIZE, config.BLOCK_SIZE))


class Texto(pygame.sprite.Sprite):

    def __init__(self, font, texto):
        self.font = font
        pygame.sprite.Sprite.__init__(self)

        imagen = self._create_text_image(texto)
        self.image = imagen
        self.rect = imagen.get_rect()
        self.z = -50
        self.rect.centerx = config.WIDTH / 2

    def _create_text_image(self, text):
        white = (255, 255 ,255)
        return self.font.render(text, 1, white)

class Item(pygame.sprite.Sprite):

    def __init__(self, imagen, imagen_bloque, codigo, fila, columna):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen_bloque
        self.image.blit(imagen, (0, 0))
        self.rect = self.image.get_rect()
        self.z = 100
        self.rect.topleft = (columna * config.BLOCK_SIZE, fila * config.BLOCK_SIZE)
        self.codigo = codigo
        self.es_boton = False

class ItemBoton(Item):

    def __init__(self, imagen, bloque, accion, x, y):
        Item.__init__(self, imagen, bloque, 1, 1, 1)
        self.es_boton = True
        self.rect.topleft = (x, y)
        self.accion = accion

class VisorItemSeleccionada(pygame.sprite.Sprite):

    def __init__(self, codigo):
        pygame.sprite.Sprite.__init__(self)
        imagen = common.load("elemento_actual.png", True, (config.BLOCK_SIZE * 2, config.BLOCK_SIZE))
        item = cargar_imagen_por_codigo(codigo)
        imagen.blit(item, (config.BLOCK_SIZE, 0))
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.right = config.WIDTH
        self.z = 100

class Estado:

    def on_exit(self):
        for x in self.items_creados:
            x.kill()

    def obtener_item_en_la_posicion(self, posicion):
        x, y = posicion
        for item in self.items_creados:
            if item.rect.collidepoint(x, y):
                return item

class EditorMenuState(Estado):
    """Estado del editor en donde se eligen items.

       Si se pulsa la tecla ``space`` se pasa al modo editor."""

    def __init__(self, editor):
        self.editor = editor
        self.items_creados = []
        self.crear_items_del_menu()
        self.crear_barra_de_botones()

        self.editor.poner_el_mouse_por_arriba()

    def crear_barra_de_botones(self):
        anterior = common.load("anterior.png", True, (config.BLOCK_SIZE, config.BLOCK_SIZE))
        siguiente = common.load("siguiente.png", True, (config.BLOCK_SIZE, config.BLOCK_SIZE))
        crear = common.load("crear.png", True, (config.BLOCK_SIZE, config.BLOCK_SIZE))

        if self.editor.nivel > 1:
            item = ItemBoton(anterior, self.editor.imagen_bloque.convert_alpha(),
                    self.editor.retroceder, config.WIDTH - config.BLOCK_SIZE * 2, 0)
            self.editor.sprites.add(item)
            self.items_creados.append(item)

        if self.editor.es_ultimo_nivel():
            item = ItemBoton(crear, self.editor.imagen_bloque.convert_alpha(),
                    self.editor.avanzar_y_crear_ese_nivel, config.WIDTH - config.BLOCK_SIZE, 0)
        else:
            item = ItemBoton(siguiente, self.editor.imagen_bloque.convert_alpha(),
                    self.editor.avanzar, config.WIDTH - config.BLOCK_SIZE, 0)

        self.editor.sprites.add(item)
        self.items_creados.append(item)

        alternar = common.load("alternar.png", True, (config.BLOCK_SIZE, config.BLOCK_SIZE))
        item = ItemBoton(alternar, self.editor.imagen_bloque.convert_alpha(), self.editor.alternar, 0, 0)
        self.editor.sprites.add(item)
        self.items_creados.append(item)

        probar = common.load("probar.png", True, (config.BLOCK_SIZE, config.BLOCK_SIZE))
        item = ItemBoton(probar, self.editor.imagen_bloque.convert_alpha(), self.editor.probar, config.BLOCK_SIZE, 0)
        self.editor.sprites.add(item)
        self.items_creados.append(item)

    def crear_items_del_menu(self):
        self.crear_item("player/ico.png", 'o', 0)
        self.crear_item("pipes/1.png", '1', 1)
        self.crear_item("pipes/2.png", '2', 2)
        self.crear_item("pipes/3.png", '3', 3)
        self.crear_item("pipes/4.png", '4', 4)
        self.crear_item("pipes/6.png", '6', 5)
        self.crear_item("pipes/7.png", '7', 6)
        self.crear_item("pipes/8.png", '8', 7)
        self.crear_item("pipes/9.png", '9', 8)
        self.crear_item("pipes/v.png", 'v', 9)
        self.crear_item("pipes/t.png", 't', 10)
        self.crear_item("pipes/n.png", 'n', 11)
        self.crear_item("pipes/f.png", 'f', 12)
        self.crear_item("pipes/r.png", 'r', 13)
        self.crear_item("pipes/y.png", 'y', 14)
        self.crear_item("front_pipes/1.png", 'z', 15)
        self.crear_item("front_pipes/2.png", 'x', 16)
        self.crear_item("front_pipes/3.png", 'c', 17)
        self.crear_item("front_pipes/4.png", 'a', 18)
        self.crear_item("front_pipes/7.png", 'q', 19)
        self.crear_item("front_pipes/9.png", 'e', 20)

    def crear_item(self, imagen, codigo, posicion):
        imagen_para_el_item = common.load(imagen, True, (config.BLOCK_SIZE, config.BLOCK_SIZE))
        dx = posicion % 14 + 1
        dy = posicion / 14 + 6
        item = Item(imagen_para_el_item, self.editor.imagen_bloque.convert_alpha(), codigo, dy, dx)
        self.editor.sprites.add(item)
        self.items_creados.append(item)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.regresar_a_modo_edicion('1')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            item_seleccionado = self.obtener_item_en_la_posicion(event.pos)

            if item_seleccionado:
                if item_seleccionado.es_boton:
                    item_seleccionado.accion()
                else:
                    self.regresar_a_modo_edicion(item_seleccionado.codigo)

    def regresar_a_modo_edicion(self, codigo_de_item):
        self.editor.change_state(EditorEditingState(self.editor, codigo_de_item))

    def on_enter(self):
        nivel = self.editor.nivel
        self.editor.avisar("MODO MENU -nivel %d- (pulsa espacio para alternar)" %(nivel))

class EditorEditingState(Estado):
    """Estado del editor en donde se editan los bloques.

       Si se pulsa la tecla ``space`` se pasa al modo menu."""

    def __init__(self, editor, codigo_de_item):
        self.editor = editor
        self.codigo_de_item = codigo_de_item
        self.items_creados = []
        self.cargar_mapa()
        self.editor.poner_el_mouse_por_arriba()
        self.crear_barra_de_botones()

    def crear_barra_de_botones(self):
        alternar = common.load("alternar.png", True, (config.BLOCK_SIZE, config.BLOCK_SIZE))
        item = ItemBoton(alternar, self.editor.imagen_bloque.convert_alpha(), self.editor.alternar, 0, 0)
        self.editor.sprites.add(item)
        self.items_creados.append(item)

        probar = common.load("probar.png", True, (config.BLOCK_SIZE, config.BLOCK_SIZE))
        item = ItemBoton(probar, self.editor.imagen_bloque.convert_alpha(), self.editor.probar, config.BLOCK_SIZE, 0)
        self.editor.sprites.add(item)
        self.items_creados.append(item)

    def cargar_mapa(self):
        mapa = self.editor.mapa

        for (fila, linea) in enumerate(mapa.map):
            for (columna, codigo) in enumerate(linea):
                try:
                    self.crear_item_por_codigo(codigo, fila, columna)
                except KeyError:
                    if config.DEBUG:
                        print "error.. no puedo imprimir el codigo", codigo
                    pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.editor.change_state(EditorMenuState(self.editor))
            elif event.key == pygame.K_F5:
                self.editor.probar_nivel()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            columna = x / config.BLOCK_SIZE
            fila = y / config.BLOCK_SIZE
            item_debajo = self.obtener_item_en_la_posicion((x, y))


            if fila < 11:
                if item_debajo:

                    if isinstance(item_debajo, ItemBoton):
                        item_debajo.accion()
                        return

                    if not isinstance(item_debajo, Item):
                        return

                    item_debajo.kill()
                    self.items_creados.remove(item_debajo)
                    self.editor.mapa.eliminar_item(fila, columna)
                else:
                    self.crear_item_por_codigo(self.codigo_de_item, fila, columna)
                    self.editor.mapa.crear_item(self.codigo_de_item, fila, columna)

    def on_exit(self):
        self.editor.mapa.guardar()
        Estado.on_exit(self)

    def crear_item_por_codigo(self, codigo, fila, columna):
        imagen_para_el_item = cargar_imagen_por_codigo(codigo)
        item = Item(imagen_para_el_item, self.editor.imagen_bloque.convert_alpha(), codigo, fila, columna)
        self.editor.sprites.add(item)
        self.items_creados.append(item)
        self.editor.poner_el_mouse_por_arriba()

    def on_enter(self):
        self.editor.avisar("MODO EDITOR (pulsa espacio para alternar, o F5 para hacer una prueba)")
        self.crear_visor_item_seleccionado()

    def crear_visor_item_seleccionado(self):
        item = VisorItemSeleccionada(self.codigo_de_item)
        self.editor.sprites.add(item)
        self.items_creados.append(item)
        self.editor.poner_el_mouse_por_arriba()


class Mapa:

    def __init__(self, nivel):
        self.cargar_nivel(nivel)

    def cargar_nivel(self, numero):
        self.numero = numero
        path = common.get_custom_level_file(numero)

        f = open(path, 'rt')

        self.map = f.readlines()

        # Se asegura de reparar cualquier archivo de mapas
        # para que todos tengan el mismo tamaño.
        for (index, x) in enumerate(self.map):
            if len(x) > config.BLOCKS_X + 1:
                self.map[index] = x[:16] + '\n'
            elif len(x) < config.BLOCKS_X + 1:
                self.map[index] = x.replace('\n', ' ') + ' ' * (config.BLOCKS_X - len(x)) + '\n'

        f.close()

    def guardar(self):
        path = common.get_custom_level_file(self.numero)
        f = open(path, 'wt')
        f.writelines(self.map)
        f.close()

    def eliminar_item(self, fila, columna):
        self.map[fila] = self.map[fila][:columna] + ' ' + self.map[fila][columna+1:]

    def crear_item(self, codigo, fila, columna):
        self.map[fila] = self.map[fila][:columna] + codigo + self.map[fila][columna+1:]

class Editor(scene.Scene):

    def __init__(self, world, nivel=1, modo_edicion=True):
        pygame.mixer.music.stop()
        scene.Scene.__init__(self, world)
        self.ultimo_avisar = None
        self.sprites = group.Group()
        font_file = common.get_ruta('FreeSans.ttf')
        self.font = pygame.font.Font(font_file, int(config.WIDTH * 0.015))
        self.imagen_bloque = common.load("bloque.png", True, (config.BLOCK_SIZE, config.BLOCK_SIZE))
        self.state = None
        self.mouse = editor_mouse.EditorMouse()
        self.sprites.add(self.mouse)
        self.mapa = Mapa(nivel)
        self.nivel = nivel

        if modo_edicion:
            self.change_state(EditorEditingState(self, 'q'))
        else:
            self.change_state(EditorMenuState(self))

        self._draw_background_and_map()

    def es_ultimo_nivel(self):
        return common.get_custom_level_file(self.nivel + 1) is None

    def avanzar_y_crear_ese_nivel(self):
        self.crear_nivel(self.nivel + 1)
        self.avanzar()

    def alternar(self):
        if isinstance(self.state, EditorEditingState):
            self.change_state(EditorMenuState(self))
        else:
            self.change_state(EditorEditingState(self, '1'))

    def probar(self):
        self.probar_nivel()

    def crear_nivel(self, nivel):
        path = common.get_custom_level_file(nivel, True)
        f = open(path, 'wt')

        template = open(common.get_ruta('level_template.txt'), 'rt')
        nivel_template = template.read()
        template.close()

        f.writelines(nivel_template)
        f.close()

    def poner_el_mouse_por_arriba(self):
        self.sprites.remove(self.mouse)
        self.sprites.add(self.mouse)

    def update(self):
        self.mouse.update()

    def draw(self, screen):
        self.sprites.clear(screen, self.background)
        pygame.display.update(self.sprites.draw(screen))

    def on_event(self, event):
        self.state.on_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.world.change_scene(menu.Menu(self.world))

    def change_state(self, new_state):
        if self.state:
            self.state.on_exit()

        self.state = new_state
        self.state.on_enter()

    def _draw_grid(self):
        "Dibuja la grilla sobre el fondo."
        for i in range(0, config.WIDTH, config.BLOCK_SIZE):
            pygame.draw.line(self.background, (255, 255, 255), (i, 0), (i, config.HEIGHT), 1)
        for i in range(0, config.HEIGHT, config.BLOCK_SIZE):
            pygame.draw.line(self.background, (255, 255, 255), (0, i), (config.WIDTH, i), 1)

    def _draw_background_and_map(self):
        "Imprime y actualiza el fondo de pantalla para usar dirtyrectagles mas adelante."
        self.background = common.load("background.jpg", False, (config.WIDTH, config.HEIGHT))
        #self.map.draw_over(self.background)
        self._draw_grid()
        self.world.screen.blit(self.background, (0, 0))

        # actualiza toda la pantalla.
        pygame.display.flip()

    def avisar(self, texto):
        sprite = Texto(self.font, texto)
        self.sprites.add(sprite)

        if self.ultimo_avisar:
            self.ultimo_avisar.kill()
            self.sprites.remove(self.ultimo_avisar)

        self.ultimo_avisar = sprite

    def probar_nivel(self):
        import game
        self.mapa.guardar()
        self.world.change_scene(game.GameCustom(self.world, level=self.mapa.numero, modo_editor=True))

    def avanzar(self):
        self.world.change_scene(Editor(self.world, self.nivel + 1, modo_edicion=False))

    def retroceder(self):
        if self.nivel > 1:
            self.world.change_scene(Editor(self.world, self.nivel - 1, modo_edicion=False))

