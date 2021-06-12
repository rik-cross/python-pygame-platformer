import pygame
import globals
import utils
from .system import *
from .colours import *
import random

class AnimationSystem(System):

    def setRequirements(self):
        self.requiredComponents = ['imagegroups']
        self.requiredTags = []

    def updateEntity(self, entity):
        ig = entity.getComponent('imagegroups')
        if entity.state in entity.getComponent('imagegroups').animationList.keys():
            ig.animationList[entity.state].update()