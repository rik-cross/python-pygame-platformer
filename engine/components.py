import pygame
import globals

class Position():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)
        self.initial = pygame.Rect(x,y,w,h)

class Animations():
    def __init__(self):
        self.animationList = {}
        self.alpha = 255
    def add(self, state, animation):
        self.animationList[state] = animation

class Animation:
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 8
    def update(self):
        # increment the timer
        self.animationTimer += 1
        # if the timer gets too high...
        if self.animationTimer >= self.animationSpeed:
            # reset the timer
            self.animationTimer = 0
            # increment the current image
            self.imageIndex += 1
            # loop back to the first image in the list
            # once the index gets too high
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0
    def draw(self, screen, x, y, flipX, flipY, zoomLevel, alpha):
        image = self.imageList[self.imageIndex]
        image.set_alpha(alpha)
        newWidth = int(image.get_rect().w * zoomLevel)
        newHeight = int(image.get_rect().h * zoomLevel)
        screen.blit(pygame.transform.scale(pygame.transform.flip(image, flipX, flipY), (newWidth, newHeight)), (x, y))

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

class Input:
    def __init__(self, up, down, left, right, b1, b2):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.b1 = b1
        self.b2 = b2

class Intention:
    def __init__(self):
        self.moveLeft = False
        self.moveRight = False
        self.jump = False
        self.zoomIn = False
        self.zoomOut = False