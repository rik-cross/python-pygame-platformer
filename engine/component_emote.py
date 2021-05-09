class Emote:
    def __init__(self, image, time=200):
        self.image = image
        self.time = time
        self.destroy = False
    def update(self):
        self.time -= 1
        if self.time <= 0:
            self.destroy = True
