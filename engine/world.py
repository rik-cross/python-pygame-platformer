from engine.entity import Entity


class World:
    def __init__(self):
        self.entities = []
        self.map = None
    def getEntitiesByTagList(self, tagList):
        entityList = []
        for e in self.entities:
            for t in tagList:
                if e.tags.has(t) and e not in entityList:
                    entityList.append(e)
        return entityList