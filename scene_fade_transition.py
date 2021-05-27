import pygame
import engine

class FadeTransitionScene(engine.TransitionScene):
    def draw(self, sm, screen):
        if self.currentPercentage < 50:
            for s in self.fromScenes:
                s.draw(sm, screen)
        else:
            if len(self.toScenes) == 0:
                if len(sm.scenes) > 1:
                    sm.scenes[-2].draw(sm, screen)
            else:
                for s in self.toScenes:
                    s.draw(sm, screen)

        # fade overlay
        overlay = pygame.Surface(pygame.display.get_surface().get_size())
        alpha = int(abs((255 - ((255/50)*self.currentPercentage))))
        overlay.set_alpha(255 - alpha)
        overlay.fill(engine.BLACK)
        screen.blit(overlay, (0,0))