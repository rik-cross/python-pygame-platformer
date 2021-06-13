import pygame

class SceneManager:
    def __init__(self):
        self.scenes = []
        self.transition = None
    def isEmpty(self):
        return len(self.scenes) == 0
    def enterScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1]._onEnter()
    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1]._onExit()
    def input(self):
        if len(self.scenes) > 0:
            self.scenes[-1]._input()
    
    def update(self):
        if self.transition is not None:
            self.transition._update()
        else:
            if len(self.scenes) > 0:
                self.scenes[-1]._update()
    
    def draw(self):
        if self.transition is not None:
            self.transition._draw()
        else:
            if len(self.scenes) > 0:
                self.scenes[-1]._draw()
        # present screen
        pygame.display.flip()
    
    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        self.enterScene()
    def pop(self):
        self.exitScene()
        self.scenes.pop()
        self.enterScene()
    def set(self, scenes):
        # pop all scenes
        while len(self.scenes) > 0:
            self.pop()
        # add new scenes
        for s in scenes:
            self.push(s)
    def setTransition(self, t):
        self.transition = t