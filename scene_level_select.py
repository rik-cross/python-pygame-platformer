import utils
import globals
import engine
import level
import scene_game
import scene_fade_transition

hues = [0, 30, 50, 90, 190, 300]

class LevelSelectScene(engine.Scene):
    def __init__(self):
    
        def loadNext():
             # keep players in a sensible order (mainly for cameras)
            utils.orderPlayers()
            # resize player cameras, depending on the number playing
            utils.setPlayerCameras()
            level.loadLevel(globals.curentLevel)
            # TODO -- shouldn't need this!
            engine.world.entities = globals.world.entities
            engine.sceneManager.push(scene_fade_transition.FadeTransitionScene([self], [scene_game.GameScene()]))

        def popScene():
            engine.sceneManager.pop()
            engine.sceneManager.push(scene_fade_transition.FadeTransitionScene([self], []))

        self.menu = engine.Menu(1500/2, 650)
        self.menu.addButton(engine.ButtonUI('Start game', actionListener=engine.ActionListener(loadNext)))
        self.menu.addButton(engine.ButtonUI('Back to player select', actionListener=engine.ActionListener(popScene)))

    def onEnter(self):
        engine.soundManager.playMusicFade('solace')
    def update(self):
        self.menu.update()
    def input(self):
        if engine.inputManager.isPressed(engine.keys.a):
            globals.curentLevel = max(globals.curentLevel-1, 1)
        if engine.inputManager.isPressed(engine.keys.d):
            globals.curentLevel = min(globals.curentLevel+1, globals.lastCompletedLevel)
            
    def draw(self):
        # background
        engine.screen.fill(engine.DARK_GREY)

        # draw level select menu
        for levelNumber in range(1, globals.maxLevel+1):
            c = engine.WHITE
            if levelNumber == globals.curentLevel:
                c = engine.GREEN
            a = 255
            if levelNumber > globals.lastCompletedLevel:
                a = 100
            engine.drawText(str(levelNumber), levelNumber*100, 100, c, a)

        self.menu.draw()