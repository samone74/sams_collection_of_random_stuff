# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 14:21:08 2017

@author: SamenLudy
"""
import random, sys, copy, os, pygame
from pygame.locals import *

class tiles(pygame.sprite.Sprite):
    """Class for all the tiles in the game"""
    def __init__(self,number,n_hori_tiles,sizetile):
        self.number = number
        self.image  = pygame.Surface((sizetile,sizetile))
        self.rect   = self.image.get_rect()
        self.rect.left = 0+sizetile *( n_hori_tiles - math.mod(number,n_hori_tiles)-1)
        self.rect.top  = 0+sizetile * (math.ceil(number/n_hori_tiles)-1)
        pygame.Surface.fill(self.image ,(0,0,0,0))        
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer        
        
  #  def update(self):

      