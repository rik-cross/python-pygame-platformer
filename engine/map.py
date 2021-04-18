import pygame

class Map:
    def __init__(self, w, h, map=None):
        self.w = w
        self.h = h
        if map is None:
            self.map = [ [ None for w in range(self.w) ] for h in range(self.h) ]
        else:
            self.map = map
    def draw(self, screen, x, y, z):
        for r in range(self.h):
            for c in range(self.w):
                material = self.map[r][c]
                if material is not None: 
                    newX = x + c*(32*z)
                    newY = y + r*(32*z)
                    newWidth = int(material.texture.get_rect().w * z)
                    newHeight = int(material.texture.get_rect().h * z)
                    material.draw(screen, newX, newY, newWidth, newHeight)