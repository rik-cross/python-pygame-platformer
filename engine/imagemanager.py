import pygame

class ImageManager:
    def __init__(self):
        self.images = {}
    def addImage(self, tag, url):
        self.images[tag] = pygame.image.load(url)
    def getImage(self, tag):
        if tag not in self.images.keys():
            return None
        return self.images[tag]
