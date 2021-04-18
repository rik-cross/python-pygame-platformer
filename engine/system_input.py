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
        if entity.input.inputFunc is not None:
            entity.input.inputFunc(inputStream, entity)
        
