from .system import *

class TextSystem(System):

    def setRequirements(self):
        self.requiredComponents = ['text']
    
    def updateEntity(self, entity):
        txt = entity.getComponent('text')
        txt.update()
        if txt.destroy:
            txt = None