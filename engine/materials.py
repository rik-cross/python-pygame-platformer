import pygame

class Material:
    def __init__(self, texture=None):
        self.texture = texture
    def draw(self, screen, x, y, w, h):
        screen.blit(pygame.transform.scale(self.texture, (w,h)), (x,y))

texture_platform = pygame.image.load('images/textures/platform.png')
material_platform = Material(texture_platform)