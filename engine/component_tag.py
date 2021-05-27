class Tag:

    def __init__(self):
        self.tags = []
    
    def add(self, tag):
        self.tags.append(tag)
    
    def has(self, tag):
        return tag in self.tags