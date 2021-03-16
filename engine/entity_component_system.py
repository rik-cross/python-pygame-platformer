import globals
import engine

def resetEntity(entity):
    pass

class Entity:
    def __init__(self):
        self.state = 'idle'
        self.type = 'normal'
        self.position = None
        self.animations = engine.Animations()
        self.direction = 'right'
        self.camera = None
        self.score = None
        self.battle = None
        self.speed = 0
        self.input = None
        self.intention = None
        self.on_ground = False
        self.acceleration = 0
        self.effect = None
        self.reset = resetEntity
        self.trauma = 0

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