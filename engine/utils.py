import pygame
from .engine import screen

def drawRect(x,y,w,h,c,a=255):
    overlay = pygame.Surface((w,h))
    overlay.set_alpha(a)
    overlay.fill(c)
    screen.blit(overlay, (x,y))