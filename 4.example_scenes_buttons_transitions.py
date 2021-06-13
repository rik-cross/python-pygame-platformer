import engine
import random

#
# create some functions to attach to the menu buttons
#

def pushSecondScene():
    engine.sceneManager.push(secondScene)

def pushThirdSceneFade():
    engine.sceneManager.setTransition(engine.TransitionCrossFade([secondScene],[thirdScene]))

def popScene():
    engine.sceneManager.pop()

def popSceneFade():
    engine.sceneManager.setTransition(engine.TransitionCrossFade([thirdScene],[]))

def changeColour():
    secondScene.bgColour = random.choice([engine.LIGHT_GREY, engine.DARK_GREY, engine.RED, engine.GREEN])

def pushFourthScene():
    engine.sceneManager.push(fourthScene)

#
# create scenes
#

class FirstScene(engine.Scene):

    def init(self):
        self.setMenu(engine.Menu(300,200,
            [engine.ButtonUI('Move to second scene', actionListener=engine.ActionListener(pushSecondScene)),
            engine.ButtonUI('Quit', actionListener=engine.ActionListener(popScene))]
        ))

    def draw(self):
        engine.screen.fill(engine.BLUE)
        engine.drawText('First scene', 50, 50, engine.WHITE, 255)

class SecondScene(engine.Scene):

    def init(self):
        self.setMenu(engine.Menu(300,200,
            [engine.ButtonUI('Back to first scene', actionListener=engine.ActionListener(popScene)),
            engine.ButtonUI('Transition to third scene', actionListener=engine.ActionListener(pushThirdSceneFade)),
            engine.ButtonUI('Change background colour', actionListener=engine.ActionListener(changeColour))]
        ))
        self.bgColour = engine.BLUE
    
    def draw(self):
        engine.screen.fill(self.bgColour)
        engine.drawText('Second scene', 50, 50, engine.WHITE, 255)

class ThirdScene(engine.Scene):

    def init(self):
        self.setMenu(engine.Menu(300, 200,
            [engine.ButtonUI('Transition to second scene', actionListener=engine.ActionListener(popSceneFade)),
            engine.ButtonUI('Fourth scene', actionListener=engine.ActionListener(pushFourthScene))]
        ))
    
    def draw(self):
        engine.screen.fill(engine.BLUE)
        engine.drawText('Third scene', 50, 50, engine.WHITE, 255)

class FourthScene(engine.Scene):

    def init(self):
        self.setMenu(engine.Menu(300, 225,
            [engine.ButtonUI('Back', actionListener=engine.ActionListener(popScene))]
        ))

    def draw(self):

        if len(engine.sceneManager.scenes) > 1:
            engine.sceneManager.scenes[-2]._draw()
        
        engine.drawRect(150,100,300,200,engine.BLACK,200)
        engine.drawText('Fourth scene', 175, 125, engine.WHITE, 255)
        
firstScene = FirstScene()
secondScene = SecondScene()
thirdScene = ThirdScene()
fourthScene = FourthScene()

#
# add scene to the engine and start
#

engine.init((600, 400), caption='Engine // Scenes, Buttons and Transitions Example')
engine.sceneManager.push(firstScene)
engine.run()