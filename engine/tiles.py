import pygame

class Tile:
    def __init__(self, texture=None, textString='none'):
        self.texture = texture
        self.textString = textString
    def draw(self, screen, x, y, w, h):
        screen.blit(pygame.transform.scale(self.texture, (w,h)), (x,y))

texture_platform = pygame.image.load('images/textures/platform.png')
tile_platform = Tile(texture_platform, 'platform')

stringToTile = {
    'platform' : tile_platform,
    'none': None
}