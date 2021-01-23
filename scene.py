import pygame

class Scene:
    def __init__(self):
        pass
    def onEnter(self):
        pass
    def onExit(self):
        pass
    def input(self, sm):
        pass
    def update(self, sm):
        pass
    def draw(self, sm):
        pass

class MainMenuScene(Scene):
    def onEnter(self):
        print('Entering main menu...')
    def onExit(self):
        print('Exiting main menu...')
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            sm.push(LevelSelectScene())
        if keys[pygame.K_z]:
            sm.pop()
    def update(self, sm):
        pass
    def draw(self, sm):
        pass

class LevelSelectScene(Scene):
    def onEnter(self):
        print('Entering level select...')
    def onExit(self):
        print('Exiting level select...')
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            sm.push(GameScene())
        if keys[pygame.K_2]:
            sm.push(GameScene())
        if keys[pygame.K_ESCAPE]:
            sm.pop()
    def update(self, sm):
        pass
    def draw(self, sm):
        pass

class GameScene(Scene):
    def onEnter(self):
        print('Entering game...')
    def onExit(self):
        print('Exiting game...')
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            sm.pop()
    def update(self, sm):
        pass
    def draw(self, sm):
        pass

class SceneManager:
    def __init__(self):
        self.scenes = []
    def isEmpty(self):
        return len(self.scenes) == 0
    def enterScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onEnter()
    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()
    def input(self):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self)
    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self)
    def draw(self):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self)
    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        self.enterScene()
    def pop(self):
        self.exitScene()
        self.scenes.pop()
        self.enterScene()
    def set(self, scene):
        # pop all scenes
        while len(self.scenes) > 0:
            self.pop()
        # add new scene
        self.push(scene)