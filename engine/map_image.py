import pygame

class MapImage:
    def __init__(self, image, x, y, z):
        self.image = image
        self.x = x
        self.y = y
        self.z = z
    def draw(self, screen, x, y, zoomLevel):
        newWidth = int(self.image.get_rect().w * zoomLevel)
        newHeight = int(self.image.get_rect().h * zoomLevel)
        screen.blit(pygame.transform.scale(self.image, (newWidth, newHeight)), (x, y))