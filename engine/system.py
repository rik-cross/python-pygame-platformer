import globals
import engine

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self):

        for entity in engine.world.entities:
            if self.check(entity):
                self.updateEntity(entity)

    def updateEntity(self, entity):
        pass