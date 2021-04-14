import pygame
import globals
import utils
from .system import *
from .colours import *
import random

class InputSystem(System):
    def check(self, entity):
        return entity.input is not None and entity.intention is not None
    def updateEntity(self, screen, inputStream, entity):
        # up = jump
        if inputStream.isDown(entity.input.up):
            entity.intention.jump = True
        else:
            entity.intention.jump = False
        # left = moveLeft
        if inputStream.isDown(entity.input.left):
            entity.intention.moveLeft = True
        else:
            entity.intention.moveLeft = False
        # right = moveRight    
        if inputStream.isDown(entity.input.right):
            entity.intention.moveRight = True
        else:
            entity.intention.moveRight = False
        # b1 = zoom out
        if inputStream.isDown(entity.input.b1):
            entity.intention.zoomOut = True
        else:
            entity.intention.zoomOut = False        
        # b2 = zoom in
        if inputStream.isDown(entity.input.b2):
            entity.intention.zoomIn = True
        else:
            entity.intention.zoomIn = False 