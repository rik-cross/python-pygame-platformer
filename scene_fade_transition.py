import pygame
import engine

class FadeTransitionScene(engine.TransitionScene):
    def draw(self):
        if self.currentPercentage < 50:
            for s in self.fromScenes:
                s.draw()
        else:
            if len(self.toScenes) == 0:
                if len(engine.sceneManager.scenes) > 1:
                    engine.sceneManager.scenes[-2].draw(engine.sceneManager, screen)
            else:
                for s in self.toScenes:
                    s.draw()

        # fade overlay
        overlay = pygame.Surface(pygame.display.get_surface().get_size())
        alpha = int(abs((255 - ((255/50)*self.currentPercentage))))
        overlay.set_alpha(255 - alpha)
        overlay.fill(engine.BLACK)
        engine.screen.blit(overlay, (0,0))