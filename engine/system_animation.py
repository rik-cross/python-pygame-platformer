import pygame
import globals
import utils
from .system import *
from .colours import *
import random

class AnimationSystem(System):
    def check(self, entity):
        return entity.imageGroups is not None
    def updateEntity(self, screen, inputStream, entity):
        entity.imageGroups.animationList[entity.state].update()