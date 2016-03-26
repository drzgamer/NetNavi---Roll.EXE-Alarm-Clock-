import sys, pygame
from pygame.locals import *
import pygame.gfxdraw

class button(object):
    """description of class"""
    
    width = 0
    height = 0
    top = 0
    left = 0
    image = pygame.image
    display = pygame.display
    

    def __init__(self, width, height, left, top, image, display):
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        print (self.left)
        self.image = image
        self.display = display

    def draw(self):
        self.display.blit(self.image, (self.left, self.top))


    def buttonListener(self, click, mouse):

        if ((self.left + self.width) > mouse[0] > self.left) and ((self.top + self.width) > mouse[1] > self.top):
            if click[0] == 1:
                return True



