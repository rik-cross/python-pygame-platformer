import pygame
import globals
import utils
from .system import *
from .colours import *
import random

class InputSystem(System):

    def check(self, entity):
        #return entity.input is not None and entity.intention is not None
        return entity.hasComponent('input') and entity.hasComponent('intention')
    
    def updateEntity(self, screen, inputStream, entity):
        #if entity.input.inputFunc is not None:
        #    entity.input.inputFunc(inputStream, entity)
        if entity.getComponent('input').inputFunc is not None:
            entity.getComponent('input').inputFunc(inputStream, entity)
        
