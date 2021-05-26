import engine
import pygame

def resetEntity(entity):
    pass

class Entity:
    ID = 0
    def __init__(self):
        self.ID = Entity.ID
        Entity.ID += 1
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
        self.effect = None
        self.reset = resetEntity
        self.trauma = 0
        self.collider = None
        self.transform = engine.Transform()
        self.motion = None
        self.tags = engine.Tag()
        self.particle_emitter = None
        self.emote = None
        self.text = None
        self.owner = self
        self.triggers = None
