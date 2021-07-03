import pygame
from .engine import sceneManager
from .engine import screen

class Scene:
    
    def __init__(self):
        self.menu = None
        self.init()
    def init(self):
        pass

    def setMenu(self, menu):
        self.menu = menu
    
    def _onEnter(self):
        self.onEnter()
    def onEnter(self):
        pass

    def _onExit(self):
        if self.menu is not None:
            self.menu.reset()
        self.onExit()
    def onExit(self):
        pass
    
    def _input(self):
        self.input()
    def _update(self):
        self.update()
        if self.menu is not None:
            self.menu.update()
    def _draw(self):
        self.draw()
        if self.menu is not None:
            self.menu.draw()

    def input(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass

    def getSceneBelow(self): # TODO
        #s = self
        #print(s in sceneManager.scenes)
        #i = sceneManager.scenes.index(self)
        return sceneManager.scenes# ........