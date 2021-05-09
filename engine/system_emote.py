from .system import *

class EmoteSystem(System):
    def check(self, entity):
        return entity.emote is not None
    def updateEntity(self, screen, inputStream, entity):
        entity.emote.update()
        if entity.emote.destroy:
            entity.emote = None