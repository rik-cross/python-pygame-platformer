from .component import Component

class TagsComponent(Component):

    def __init__(self):
        self.key = 'tags'
        self.tags = []
    
    def add(self, tag):
        self.tags.append(tag)
    
    def has(self, tag):
        return tag in self.tags