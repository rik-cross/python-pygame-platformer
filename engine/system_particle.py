from .system import *

class ParticleSystem(System):
    def check(self, entity):
        return entity.particle_emitter is not None
    def updateEntity(self, screen, inputStream, entity):
        entity.particle_emitter.update(entity.position.rect.x, entity.position.rect.y)
        if entity.particle_emitter.destroy:
            entity.particle_emitter = None