import pygame

class Motion:
    def __init__(self, velocity=pygame.math.Vector2(), acceleration=pygame.math.Vector2()):
        self.velocity = velocity
        self.initialVelocity = velocity
        self.acceleration = acceleration
        self.initialAcceleration = acceleration
    def reset(self):
        self.velocity = self.initialVelocity
        self.acceleration = self.initialAcceleration