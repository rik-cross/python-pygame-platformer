import engine
import scene_fade_transition
import scene_player_select

class MainMenuScene(engine.Scene):

    def init(self):

        def loadNext():
            engine.sceneManager.push(scene_fade_transition.FadeTransitionScene([self], [scene_player_select.PlayerSelectScene()]))

        def quitGame():
            engine.sceneManager.pop()

        self.menu = engine.Menu(1500/2, 650)
        self.menu.addButton(engine.ButtonUI('New game', actionListener=engine.ActionListener(loadNext)))
        self.menu.addButton(engine.ButtonUI('Quit', actionListener=engine.ActionListener(quitGame)))

    def onEnter(self):       
        engine.soundManager.playMusicFade('solace')
    #def update(self):
    #    self.mainMenu.update()
    def draw(self):
        # background
        engine.screen.fill(engine.DARK_GREY)
        #self.mainMenu.draw()