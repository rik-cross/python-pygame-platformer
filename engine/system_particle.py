from .system import *

class ParticleSystem(System):

    def setRequirements(self):
        self.requiredComponents = ['emitter']

    def updateEntity(self, entity):
        emt = entity.getComponent('emitter')
        pos = entity.getComponent('position')
        emt.update(pos.rect.x, pos.rect.y)
        if emt.destroy:
            emt = None