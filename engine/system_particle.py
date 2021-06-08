from .system import *

class ParticleSystem(System):

    def check(self, entity):
        return entity.hasComponent('emitter') #particle_emitter is not None
    
    def updateEntity(self, screen, entity):
        emt = entity.getComponent('emitter')
        pos = entity.getComponent('position')
        emt.update(pos.rect.x, pos.rect.y)
        if emt.destroy:
            emt = None