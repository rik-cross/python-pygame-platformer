import pygame
from .component import Component

class Collider(Component):

    def __init__(self, offsetX, offsetY, w, h):
        self.rect = pygame.Rect(offsetX, offsetY, w, h)
    
    def collidingWith(self, otherEntity):
        if self.rect is None or otherEntity.rect is None:
            return False
        return self.rect.colliderect(otherEntity.rect)