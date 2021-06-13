class Scene:
    
    def __init__(self):
        self.menu = None
        self.init()
    def init(self):
        pass

    def setMenu(self, menu):
        self.menu = menu
    
    def __del__(self):
    #    self.unload()
    #def unload(self):
        pass
    
    def onEnter(self):
        pass
    def onExit(self):
        pass
    
    def _input(self):
        self.input()
    def _update(self):
        self.update()
        if self.menu is not None:
            self.menu.update()
    def _draw(self):
        self.draw()
        if self.menu is not None:
            self.menu.draw()

    def input(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass