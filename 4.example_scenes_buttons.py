import engine
import random

#
# create some functions to attach to the menu buttons
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

    def init(self):
        self.setMenu(engine.Menu(300,200,
            [engine.ButtonUI('Move to second scene', actionListener=engine.ActionListener(pushSecondScene)),
            engine.ButtonUI('Quit',actionListener=engine.ActionListener(popScene))]
        ))

    def draw(self):
        engine.screen.fill(engine.BLUE)
        engine.drawText('First scene',50,50,engine.WHITE,255)

class SecondScene(engine.Scene):

    def init(self):
        self.setMenu(engine.Menu(300,200,
            [engine.ButtonUI('Move to first scene', actionListener=engine.ActionListener(popScene)),
            engine.ButtonUI('Change colour',actionListener=engine.ActionListener(changeColour))]
        ))
        self.bgColour = engine.RED
    
    def draw(self):
        engine.screen.fill(self.bgColour)
        engine.drawText('Second scene',50,50,engine.WHITE,255)

firstScene = FirstScene()
secondScene = SecondScene()

#
# add scene to the engine and start
#

engine.init((600, 400), caption='Engine // Scenes and Buttons Example')
engine.sceneManager.push(firstScene)
engine.run()