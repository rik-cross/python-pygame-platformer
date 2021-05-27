import engine
import scene_fade_transition
import scene_player_select

class MainMenuScene(engine.Scene):

    def __init__(self):

        def loadNext():
            engine.sceneManager.push(scene_fade_transition.FadeTransitionScene([self], [scene_player_select.PlayerSelectScene()]))

        def quitGame():
            engine.sceneManager.pop()

        self.mainMenu = engine.Menu(1500/2, 650)
        self.mainMenu.addButton(engine.ButtonUI('New game', actionListener=engine.ActionListener(loadNext)))
        self.mainMenu.addButton(engine.ButtonUI('Quit', actionListener=engine.ActionListener(quitGame)))

    def onEnter(self):       
        engine.soundManager.playMusicFade('solace')
    def update(self, sm, inputStream):
        self.mainMenu.update(inputStream)
    def draw(self, sm, screen):
        # background
        screen.fill(engine.DARK_GREY)
        self.mainMenu.draw(screen)