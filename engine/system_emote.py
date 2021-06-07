from .system import System

class EmoteSystem(System):

    def check(self, entity):
        return entity.hasComponent('emote') #emote is not None
    
    def updateEntity(self, screen, inputStream, entity):
        em = entity.getComponent('emote')
        em.update()
        if em.destroy:
            em = None