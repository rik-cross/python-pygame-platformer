import pygame

class Position:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)
        self.initial = pygame.Rect(x,y,w,h)