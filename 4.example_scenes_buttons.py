import engine
import random

#
# create some functions to attach to the buttons
#

def pushSecondScene():
    engine.sceneManager.push(secondScene)

def popScene():
    engine.sceneManager.pop()

def changeColour():
    secondScene.bgColour = random.choice([engine.LIGHT_GREY, engine.DARK_GREY, engine.GREEN, engine.BLUE])

#
# create 2 scenes
#

class FirstScene(engine.Scene):
    def __init__(self):
        self.menu = engine.Menu(300,200,
            [engine.ButtonUI('Move to second scene', actionListener=engine.ActionListener(pushSecondScene))]
        )
        self.menu.addButton(engine.ButtonUI('Quit',actionListener=engine.ActionListener(popScene)))
    def update(self):
        self.menu.update()
    def draw(self):
        engine.screen.fill(engine.BLUE)
        engine.drawText('First scene',50,50,engine.WHITE,255)
        self.menu.draw()

class SecondScene(engine.Scene):
    def __init__(self):
        self.menu = engine.Menu(300,200,
            [engine.ButtonUI('Move to first scene', actionListener=engine.ActionListener(popScene))]
        )
        self.menu.addButton(engine.ButtonUI('Change colour',actionListener=engine.ActionListener(changeColour)))
        self.bgColour = engine.RED
    def update(self):
        self.menu.update()
    def draw(self):
        engine.screen.fill(self.bgColour)
        engine.drawText('Second scene',50,50,engine.WHITE,255)
        self.menu.draw()

firstScene = FirstScene()
secondScene = SecondScene()

#
# add scene to the engine and start
#

engine.init((600, 400), caption='Engine // Scenes and Buttons Example')
engine.sceneManager.push(firstScene)
engine.run()