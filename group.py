# -*- coding: utf-8 -*-
# Ayni
#
# Copyright 2009 - Gcoop <info@gcoop.coop>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import pygame
import pprint
import config

class Group(pygame.sprite.OrderedUpdates):

    def __init__(self, *k):
        pygame.sprite.OrderedUpdates.__init__(self, *k)

    def sort_by_z(self):
        sprites = self.sprites()
        sprites.sort()
        self.empty()

        for x in sprites:
            self.add(x)

    def draw(self, surface):
       spritedict = self.spritedict
       surface_blit = surface.blit
       dirty = self.lostsprites
       self.lostsprites = []
       dirty_append = dirty.append

       for s in self.sprites():
           r = spritedict[s]

           rect = pygame.Rect(s.rect)

           if config.LOWRES:
               rect.x /= 2
               rect.y /= 2

           newrect = surface_blit(s.image, rect)
           if r is 0:
               dirty_append(newrect)
           else:
               if newrect.colliderect(r):
                   dirty_append(newrect.union(r))
               else:
                   dirty_append(newrect)
                   dirty_append(r)
           spritedict[s] = newrect

       return dirty
