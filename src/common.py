import os.path
import pygame
import pytweener
import config
import shutil

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

def get_level_file(level):
    "Devuelve la ruta al mapa original (desde el directorio data)."
    nivel = '%d.txt' % level

    # si no existe en home ni se va a escribir devolvemos el archivo
    # en el directorio data
    if os.path.isfile(get_ruta(os.path.join('map', nivel))):
        return get_ruta(os.path.join('map', nivel))

    return None

def get_custom_level_file(level, retornar_ruta_si_no_existe=False):
    "Devuelve la ruta al mapa modificado por el usuario (desde el directorio home)."
    nivel = '%d.txt' % level

    homedir = os.path.expanduser('~/.ayni')

    # TODO: extraer en nueva funcion: si no existen los niveles los tiene que crear.
    print "*" * 10
    print "*" * 10

    if not os.path.exists(homedir):
        print "Generando el directorio: " + homedir
        os.makedirs(homedir)
        print "Creando niveles de ejemplo."
        shutil.copy(get_ruta(os.path.join('mapas_template', "1.txt")), os.path.join(homedir, "1.txt"))
        shutil.copy(get_ruta(os.path.join('mapas_template', "2.txt")), os.path.join(homedir, "2.txt"))

    #si el archivo de nivel ya existe en el directorio en home o
    #se va escribir en el archivo devolvemos la ruta al archivo
    #en home.
    if os.path.isfile(os.path.join(homedir, nivel)):
        return os.path.join(homedir, nivel)

    if retornar_ruta_si_no_existe:
        return os.path.join(homedir, nivel)
    else:
        return None

def play_music(name):
    "Comienza a reproducir una musica del directorio 'music'."
    pygame.mixer.music.fadeout(200)
    pygame.mixer.music.load(get_ruta(os.path.join('music', name)))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
