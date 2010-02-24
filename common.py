import pygame
import pytweener

tweener = pytweener.Tweener()

def load(filepath, use_alpha=False):
    "Carga una imagen optimizando la velocidad de impresion."

    image = pygame.image.load("data/" + filepath)

    if use_alpha:
        return image.convert_alpha()
    
    return image.convert()
