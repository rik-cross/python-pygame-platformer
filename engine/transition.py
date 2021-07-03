import pygame
from .colours import *
from .engine import sceneManager, screen

# TODO -- I don't think you need 'fronScenes' -- just draw the top
# of the sceneManager stack?

class Transition:

    def __init__(self, fromScenes, toScenes):
        self.fromScenes = fromScenes
        self.toScenes = toScenes
        self.currentPercentage = 0
        self.init()

    def init(self):
        pass

    def onComplete(self):
        if len(self.toScenes) == 0:
                sceneManager.pop()
        else:
            for s in self.toScenes:
                sceneManager.push(s)

    def _update(self):
        self.currentPercentage = min(100, self.currentPercentage+2)

        for fs in self.fromScenes:
            fs._update()

        for ts in self.toScenes:
            ts._update()

        if self.currentPercentage == 100:
            
            sceneManager.transition = None
            self.onComplete()

        self.update()
    def update(self):
        pass

    def _draw(self):
        self.draw()
    def draw(self):
        pass

class TransitionCrossFade(Transition):

    def draw(self):

        if self.currentPercentage < 50:
            sceneManager.getTopScene()._draw()
            for s in self.fromScenes:
                s._draw()
        else:
            if len(self.toScenes) == 0:
                if len(sceneManager.scenes) > 1:
                    sceneManager.scenes[-2]._draw()
            else:
                for s in self.toScenes:
                    s._draw()

        # fade overlay
        overlay = pygame.Surface(pygame.display.get_surface().get_size())
        alpha = int(abs((255 - ((255/50)*self.currentPercentage))))
        overlay.set_alpha(255 - alpha)
        overlay.fill(BLACK)
        screen.blit(overlay, (0,0))

#class TransitionFadeIn(Transition):
#    
#    def onComplete(self):
#        for s in self.toScenes:
#            #print('push')
#            sceneManager.push(s)

#    def draw(self):
        
#        for s in self.fromScenes:
#            s._draw()

#        alpha = int(self.currentPercentage * 2.55) #int(abs((255 - ((255/50)*self.currentPercentage))))
#        for s in self.toScenes:
#            s._draw()

#class TransitionFadeOut(Transition):
    
#    def draw(self):

#        for s in self.fromScenes:
#            s._draw()

#        alpha = 255 - int(self.currentPercentage * 2.55) #int(abs((255 - ((255/50)*self.currentPercentage))))
#        for s in self.toScenes:
#            s._draw()
