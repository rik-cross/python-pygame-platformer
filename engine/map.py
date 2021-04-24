import pygame
import pickle
import math
from .tiles import *

class Map:

    def __init__(self, w, h, map=None, tileSize=32):
        self.w = w
        self.h = h
        self.tileSize = tileSize
        if map is None:
            self.map = [ [ tile_empty for w in range(self.w) ] for h in range(self.h) ]
        elif isinstance(map, str):
            self.loadFromFile(map)
        else:
            self.map = map
    
    def loadFromFile(self, filename):
        filename = 'levels/' + filename + '.lvl'
        mapToLoad = pickle.load( open( filename, "rb" ) )
        nmap = []
        for r in range(len(mapToLoad)):
            row = []
            for c in mapToLoad[r]:
                row.append(stringToTile[c])
            nmap.append(row)
        self.map = nmap
    
    def saveToFile(self, filename):
        filename = 'levels/' + filename + '.lvl'
        mapToSave = []
        for r in range(len(self.map)):
            rowToSave = []
            for c in self.map[r]:
                rowToSave.append(c.textString)
            mapToSave.append(rowToSave)
        pickle.dump( mapToSave, open( filename, "wb" ) )
    
    def getTileAtPosition(self, x, y):
        xTile = int(x // self.tileSize)
        yTile = int(y // self.tileSize)
        return self.map[yTile][xTile]

    def draw(self, screen, x, y, z):
        for r in range(self.h):
            for c in range(self.w):
                tile = self.map[r][c]
                if tile.texture is not None: 
                    newX = x + c*(self.tileSize*z)
                    newY = y + r*(self.tileSize*z)
                    newWidth = math.ceil(tile.texture.get_rect().w * z)
                    newHeight = math.ceil(tile.texture.get_rect().h * z)
                    tile.draw(screen, newX, newY, newWidth, newHeight)