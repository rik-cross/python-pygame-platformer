import engine

#
# Create a simple example game scene
#

class MainScene(engine.Scene):
    def draw(self, sm, screen):
        screen.fill(engine.BLUE)

mainGameScene = MainScene()

#
# Add scene to the engine and start
#

engine.init((1500,800), 'Simple Example')
engine.sceneManager.push(mainGameScene)
engine.run()