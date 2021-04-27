import pygame
import pickle
import math
from .tiles import *

MAPSIZE = 256

class Map:

    def __init__(self, map=None, tileSize=32):
        self.tileSize = tileSize
        if map is None:
            self.map = [ [ Tile.tiles['none'] for w in range(MAPSIZE) ] for h in range(MAPSIZE) ]
        elif isinstance(map, str):
            self.loadFromFile(map)
        else:
            self.map = map
        self.setDimensions() 

    def setDimensions(self):

        # calculate height
        lastNonEmptyRow = 0
        for row in range(len(self.map)):
            for column in self.map[row]:
                if column is not Tile.tiles['none']:
                    lastNonEmptyRow = row + 1
                    break

        # calculate width
        longestRow = 0
        for row in self.map:
            for tileNumber in range(len(row)):
                if row[tileNumber] is not Tile.tiles['none']:
                    if tileNumber > longestRow:
                        longestRow = tileNumber + 1

        # set dimensions
        self.h_map = lastNonEmptyRow
        self.w_map = longestRow
        self.h_real = self.h_map * self.tileSize
        self.w_real = self.w_map * self.tileSize

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
        self.setDimensions()
    
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