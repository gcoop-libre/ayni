import os.path
import pygame
import pytweener
import config

tweener = pytweener.Tweener()

def load(filepath, use_alpha=False, scale=None):
    "Carga una imagen optimizando la velocidad de impresion."
    image = pygame.image.load(get_ruta(filepath))

    if scale is not None:
        width,height = scale
        #si una de las dos dimensiones de scale es 0 la
        #calculamos para mantener la proporcion original
        if width == 0 and height != 0:
            width = image.get_width() * height / image.get_height()

        elif height == 0 and width != 0:
            height = image.get_height() * width / image.get_width()

        image = pygame.transform.smoothscale(image, (int(width), int(height)))

    if use_alpha:
        return image.convert_alpha()

    return image.convert()

def get_ruta(filepath):
    "Devuelve la ruta absoluta al archivo en filepath."
    basedir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(basedir, 'data', filepath)

def get_level_file(level, write=False):
    "Devuelve la ruta al archivo correspondiente el nivel recibido."

    nivel = '%d.txt' % level
    basedir = os.path.dirname(os.path.realpath(__file__))
    homedir = os.path.expanduser('~/.ayni')
    if not os.path.exists(homedir):
        os.makedirs(homedir)

    #si el archivo de nivel ya existe en el directorio en home o 
    #se va escribir en el archivo devolvemos la ruta al archivo
    #en home.
    if os.path.isfile(os.path.join(homedir, nivel)) or write:
        return os.path.join(homedir, nivel)

    #si no existe en home ni se va a escribir devolvemos el archivo 
    #en el directorio data
    if os.path.isfile(get_ruta(os.path.join('map', nivel))):
        return get_ruta(os.path.join('map', nivel))

    return None

