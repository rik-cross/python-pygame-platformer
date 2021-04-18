import engine

def resetEntity(entity):
    pass

class Entity:
    def __init__(self):
        self.state = 'idle'
        self.type = 'normal'
        self.position = None
        self.imageGroups = engine.ImageGroups()
        self.direction = 'right'
        self.camera = None
        self.score = None
        self.battle = None
        self.input = None
        self.intention = None
        self.on_ground = False
        self.acceleration = 0
        self.initialAcceleration = 0
        self.effect = None
        self.reset = resetEntity
        self.trauma = 0
        self.collider = None
        self.transform = engine.Transform()
        self.motion = None
        self.tags = engine.Tag()