import pygame
import pickle
import math
from .tiles import *

class Map:

    def __init__(self, w, h, map=None):
        self.w = w
        self.h = h
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
                #if c is None:
                #    rowToSave.append('none')
                #else:
                rowToSave.append(c.textString)
            mapToSave.append(rowToSave)
        pickle.dump( mapToSave, open( filename, "wb" ) )
    
    def getTileAtPosition(self, x, y):
        xTile = x // 32
        yTile = y // 32
        #if self.map[yTile][xTile] is None:
        #    return None
        return self.map[yTile][xTile]

    def draw(self, screen, x, y, z):
        for r in range(self.h):
            for c in range(self.w):
                tile = self.map[r][c]
                if tile.texture is not None: 
                    newX = x + c*(32*z)
                    newY = y + r*(32*z)
                    newWidth = math.ceil(tile.texture.get_rect().w * z)
                    newHeight = math.ceil(tile.texture.get_rect().h * z)
                    tile.draw(screen, newX, newY, newWidth, newHeight)