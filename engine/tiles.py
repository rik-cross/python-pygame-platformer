import pygame

class Tile:

    tiles = {}

    @classmethod
    def addTile(cls, tileString, tile):
        cls.tiles[tileString] = tile

    def __init__(self, texture=None, solid=False):
        self.texture = texture
        self.solid = solid
    
    def draw(self, screen, x, y, w, h):
        if self.texture is None:
            return
        screen.blit(pygame.transform.scale(self.texture, (w,h)), (x,y))

# add the default empty tile
Tile.addTile('none', Tile())