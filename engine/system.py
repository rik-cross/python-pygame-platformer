import globals
import engine

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, screen=None, inputStream=None):
        for entity in globals.world.entities:
            if self.check(entity):
                self.updateEntity(screen, inputStream, entity)
    def updateEntity(self, screen, inputStream, entity):
        pass