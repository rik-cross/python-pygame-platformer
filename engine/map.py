import pygame
import pickle
import math
from .tiles import *

class Map:

    def __init__(self, map=None, mapWidth=64, mapHeight=64, tileSize=32):
        self.tileSize = tileSize
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        if map is None:
            self.map = [ [ Tile.tiles['none'] for w in range(self.mapWidth) ] for h in range(self.mapHeight) ]
        elif isinstance(map, str):
            self.loadFromFile(map)
        else:
            self.map = map
        self.setDimensions() 

    def setDimensions(self):
        self.h_map = self.mapHeight
        self.w_map = self.mapWidth
        self.h_real = self.mapHeight * self.tileSize
        self.w_real = self.mapWidth * self.tileSize

    def loadFromFile(self, filename):
        filename = 'levels/' + filename + '.lvl'
        mapToLoad = pickle.load( open( filename, "rb" ) )
        nmap = []
        for r in range(len(mapToLoad)):
            row = []
            for c in mapToLoad[r]:
                row.append(Tile.tiles[c])
            nmap.append(row)
        self.map = nmap
        self.setDimensions()
    
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
        if self.map is None:
            return Tile.tiles['none']
        xTile = int(x // self.tileSize)
        yTile = int(y // self.tileSize)
        return self.map[yTile][xTile]

    def draw(self, screen, x, y, z):
        if self.map is None:
            return
        for r in range(self.h_map):
            for c in range(self.w_map):
                tile = self.map[r][c]
                if tile.texture is not None: 
                    newX = x + c*(self.tileSize*z)
                    newY = y + r*(self.tileSize*z)
                    newWidth = math.ceil(self.tileSize * z)
                    newHeight = math.ceil(self.tileSize * z)
                    tile.draw(screen, newX, newY, newWidth, newHeight)