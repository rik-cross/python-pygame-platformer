from .system import *

class TextSystem(System):
    def check(self, entity):
        return entity.text is not None
    def updateEntity(self, screen, inputStream, entity):
        entity.text.update()
        if entity.text.destroy:
            entity.text = None