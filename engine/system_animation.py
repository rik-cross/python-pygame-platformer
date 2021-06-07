import pygame
import globals
import utils
from .system import *
from .colours import *
import random

class AnimationSystem(System):

    def check(self, entity):
        return entity.hasComponent('imagegroups') #entity.imageGroups is not None
    
    def updateEntity(self, screen, inputStream, entity):
        ig = entity.getComponent('imagegroups')
        ig.animationList[entity.state].update()