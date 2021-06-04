import pygame
from .component import Component
from .engine import *

class CameraComponent(Component):

    def __init__(self, x, y, w, h):
        self.key = 'camera'
        self.rect = pygame.Rect(x,y,w,h)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
        self.zoomLevel = 1

        self.zoomPerFrame = 0
        self.targetZoom = self.zoomLevel

        self.targetX = 0
        self.targetY = 0
        self.movementPerFrameX = 0
        self.movementPerFrameY = 0
    
    def setZoomLevel(self, level):
        self.zoomLevel = level
    
    def zoomTo(self, level, overFrames=60):
        self.targetZoom = level
        self.zoomPerFrame = (self.targetZoom - self.zoomLevel) / overFrames

    def moveTo(self, x, y, overFrames=60):
        self.entityToTrack = None
        self.targetX = x
        self.targetY = y
        self.movementPerFrameX = (self.targetX - self.worldX) / overFrames
        self.movementPerFrameY = (self.targetY - self.worldY) / overFrames

    def setWorldPos(self, x, y):
        newX = x
        newY = y
  
        if world is not None and world.map is not None:

            # calculate x value

            # if world narrower than camera:
            if (self.rect.w) > (world.map.w_real*self.zoomLevel):
                newX = (world.map.w_real / 2)
            else:
                newX = max(newX, (self.rect.w/self.zoomLevel)/2)
                newX = min(newX, ( ((world.map.w_real) - (self.rect.w/2/self.zoomLevel)) ) )

            # calculate y value

            # if world narrower than camera:
            if self.rect.h > (world.map.h_real*self.zoomLevel):
                newY = (world.map.h_real / 2)
            else:
                newY = max(newY, (self.rect.h/self.zoomLevel/2))
                newY = min(newY, ( ((world.map.h_real) - (self.rect.h/2/self.zoomLevel)) ) )

        self.worldX = newX
        self.worldY = newY

    def trackEntity(self, entity):
        self.entityToTrack = entity