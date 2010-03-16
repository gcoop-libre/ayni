import pygame
import pytweener
import config

tweener = pytweener.Tweener()

def load(filepath, use_alpha=False):
    "Carga una imagen optimizando la velocidad de impresion."

    image = pygame.image.load("data/" + filepath)

    if config.LOWRES:
        image = pygame.transform.rotozoom(image, 0, 0.5)

    if use_alpha:
        return image.convert_alpha()

    
    return image.convert()
