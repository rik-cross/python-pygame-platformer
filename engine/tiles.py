import pygame

class Tile:
    def __init__(self, texture=None, textString='none', solid=False):
        self.texture = texture
        self.textString = textString
        self.solid = solid
    def draw(self, screen, x, y, w, h):
        if self.texture is None:
            return
        screen.blit(pygame.transform.scale(self.texture, (w,h)), (x,y))

texture_platform = pygame.image.load('images/textures/platform.png')
tile_platform = Tile(texture_platform, 'platform', True)

tile_empty = Tile()

stringToTile = {
    'platform' : tile_platform,
    'none': tile_empty
}