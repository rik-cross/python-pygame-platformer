from .system import *

class TextSystem(System):

    def check(self, entity):
        return entity.hasComponent('text') #entity.text is not None
    
    def updateEntity(self, screen, entity):
        txt = entity.getComponent('text')
        txt.update()
        if txt.destroy:
            txt = None