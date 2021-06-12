from engine.system import System
import engine
import scene_win
import scene_lose
import gamesystems
import scene_fade_transition
import globals

class GameScene(engine.Scene):
    #def __del__(self):
    #    engine.world.clear()
    def onEnter(self):
        engine.soundManager.playMusicFade('dawn')
    def unload(self):
        engine.world.clear()
    def input(self):
        if engine.inputManager.isPressed(engine.keys.esc):
            engine.sceneManager.pop()
            engine.sceneManager.push(scene_fade_transition.FadeTransitionScene([self], []))
        if globals.world.isWon():
            # update the level select map accessible levels
            nextLevel = min(globals.curentLevel+1, globals.maxLevel)
            levelToUnlock = max(nextLevel, globals.lastCompletedLevel)
            globals.lastCompletedLevel = levelToUnlock
            globals.curentLevel = nextLevel
            engine.sceneManager.push(scene_win.WinScene())
        if globals.world.isLost():
            engine.sceneManager.push(scene_lose.LoseScene())