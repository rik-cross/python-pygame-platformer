class ActionListener:
    def __init__(self, f):
        self.action = f
    def execute(self):
        self.action()