import pygame

class Transform:
    def __init__(self, position=pygame.math.Vector2(), rotation=90):
        self.position = position
        self.initialPosition = position
        self.rotation = rotation
        self.initialRotation = rotation
    def reset(self):
        self.position = self.initialPosition
        self.rotation = self.initialRotation