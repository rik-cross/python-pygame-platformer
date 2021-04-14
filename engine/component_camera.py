import pygame
import globals

class Camera:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
        self.zoomLevel = 1
    def setWorldPos(self, x, y):
        newX = x
        newY = y
  
        if globals.world is not None:

            # calculate x value

            # if world narrower than camera:
            if (self.rect.w) > (globals.world.size[0]*self.zoomLevel):
                newX = (globals.world.size[0] / 2)
            else:
                newX = max(newX, (self.rect.w/self.zoomLevel)/2)
                newX = min(newX, ( ((globals.world.size[0]) - (self.rect.w/2/self.zoomLevel)) ) )

            # calculate y value

            # if world narrower than camera:
            if self.rect.h > (globals.world.size[1]*self.zoomLevel):
                newY = (globals.world.size[1] / 2)
            else:
                newY = max(newY, (self.rect.h/self.zoomLevel/2))
                newY = min(newY, ( ((globals.world.size[1]) - (self.rect.h/2/self.zoomLevel)) ) )

        self.worldX = newX
        self.worldY = newY

    def trackEntity(self, e):
        self.entityToTrack = e