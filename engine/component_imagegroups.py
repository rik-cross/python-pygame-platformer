class ImageGroups:
    def __init__(self):
        self.animationList = {}
        self.alpha = 255
        self.hue = None
    def add(self, state, animation):
        self.animationList[state] = animation