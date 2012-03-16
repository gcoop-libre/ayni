import pygame
import pytweener
import config

tweener = pytweener.Tweener()

def load(filepath, use_alpha=False, scale=None):
    "Carga una imagen optimizando la velocidad de impresion."

    image = pygame.image.load("data/" + filepath)

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
