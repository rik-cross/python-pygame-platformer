import engine
import scene_main_menu
import scene_level_select
import utils
import pygame
import scene_player_select
import scene_game
import scene_fade_transition

class WinScene(engine.Scene):
    def __init__(self):
        self.alpha = 0

        def back():
            engine.sceneManager.set([scene_fade_transition.FadeTransitionScene([scene_game.GameScene(), self], [scene_main_menu.MainMenuScene(), scene_player_select.PlayerSelectScene(), scene_level_select.LevelSelectScene()])])
        
        self.menu = engine.Menu(1500/2, 650)
        self.menu.addButton(engine.ButtonUI('Back', actionListener=engine.ActionListener(back)))

    def update(self, sm):
        self.alpha = min(255, self.alpha + 10)
        self.menu.update()
    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # draw a transparent bg
        bgSurf = pygame.Surface(pygame.display.get_surface().get_size())
        bgSurf.fill((engine.BLACK))
        utils.blit_alpha(screen, bgSurf, (0,0), self.alpha * 0.7)

        engine.drawText(screen, 'You win!', 50, 50, engine.WHITE, self.alpha)
        self.menu.draw(screen)