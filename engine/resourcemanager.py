import pygame

class ResourceManager:
    
    def __init__(self):
        self.fonts = {}
    
    def addFont(self, tag, url, size=24):
        self.fonts[tag] = pygame.font.Font(url, size)
    
    def getFont(self, tag):
        if tag not in self.fonts.keys():
            return None
        return self.fonts[tag]