import pygame
import os


class Sheet:
    "Representa una grilla con varios cuadros de animacion."

    def __init__(self, image, cols):
        self._create_image_sheet(image, cols)
        self.cols = cols
        self.frame = 0

    def _create_image_sheet(self, image, cols):
        image_width = image.get_width()
        frame_width = image_width / cols
        dw = image_width % cols

        if dw > 0:
            print "Cuidado, la imagen no es exactamente divisible."
            print "   quitando", dw, "pixeles de la imagen."
            image_width -= dw


        frame_height = image_height = image.get_height()
        images = []

        for x in range(0, image_width, frame_width):
            rect = pygame.Rect(x, 0, frame_width, frame_height)
            images.append(image.subsurface(rect).copy())

        self.images = images
        self.flipped_images = [pygame.transform.flip(x, True, False) 
                                    for x in images]

    def set_frame(self, frame):
        self.frame = frame

    def get_image(self, flipped=False):
        if flipped:
            return self.flipped_images[self.frame]
        else:
            return self.images[self.frame]

    def next_frame(self):
        "Avanza el cuadro de animacion y retorna True si reinicia la secuencia."
        self.frame += 1

        if self.frame >= len(self.images):
            self.frame = 0
            return True

class Animation:
    "Representa una animacion aplicada a una grilla."

    def __init__(self, sheet, delay, sequence, stop_when_finish=False):
        self.step_in_sequence = 0
        self.sheet = sheet
        self.delay = delay
        self.reset()
        self.sequence = sequence
        self.stop_when_finish = stop_when_finish

    def reset(self):
        self.delay_counter = 0

    def update(self):
        "Avanza en la animacion y retorna True si ha reiniciado."
        self.delay_counter += 1

        if self.delay_counter >= self.delay:
            self.reset()
            return self.next_frame()

    def get_image(self, flipped=False):
        return self.sheet.get_image(flipped)

    def next_frame(self):
        "Avanza en la secuencia y retorna True si la animacion termina."
        was_restarted = False
        self.step_in_sequence += 1

        if self.step_in_sequence >= len(self.sequence):
            if self.stop_when_finish:
                self.step_in_sequence -= 1
            else:
                self.step_in_sequence = 0
                was_restarted = True

        frame_to_show = self.sequence[self.step_in_sequence]
        self.sheet.set_frame(frame_to_show)

        return was_restarted
