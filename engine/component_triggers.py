#from engine.world import World
import pygame
import engine

class Triggers:
    def __init__(self):
        # a list of Interaction objects
        self.triggerList = []

class Trigger:
    def __init__(self, boundingBox=None):
        self.boundingBox = boundingBox
        # to keep track of which entities the trigger is colliding with
        self.last = []
        self.current = []
    def onCollide(self):
        pass
    def onCollisionEnter(self):
        pass
    def onCollisionExit(self):
        pass

class SignPlayerTrigger(Trigger):
    def onEnter(self, e):
        #for entity in engine.world.getEntitiesByIDList(self.current):
        #    pass
        e.text = engine.Text('Welcome to Level 1. Collect all of the coins.')
    def onStay(self, e):
        pass
    def onExit(self, e):
        if not self.current:
            e.text = None