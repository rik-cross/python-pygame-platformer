import pygame

class Collider:
    def __init__(self, offsetX, offsetY, w, h):
        self.rect = pygame.Rect(offsetX,offsetY,w,h)