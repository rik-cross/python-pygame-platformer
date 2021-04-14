import pygame

class Transform:
    def __init__(self, motion=pygame.math.Vector2(), acceleration=pygame.math.Vector2()):
        self.motion = motion
        self.acceleration = acceleration