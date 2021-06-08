import globals
import engine

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, screen=None):

        for entity in engine.world.entities:
            if self.check(entity):
                self.updateEntity(screen, entity)

    def updateEntity(self, screen, entity):
        pass