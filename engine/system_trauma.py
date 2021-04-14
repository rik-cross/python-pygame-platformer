import pygame
import globals
import utils
from .system import *
from .colours import *
import random

class TraumaSystem(System):
    def check(self, entity):
        return entity.trauma is not None
    def updateEntity(self, screen, inputStream, entity):    
        entity.trauma =  max(0, entity.trauma - 0.01 )