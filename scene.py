import pygame
import utils
import globals
import engine
import ui
import level
import gamesystems

class MainMenuScene(engine.Scene):
    def __init__(self):
        self.enter = ui.ButtonUI(pygame.K_RETURN, '[Enter=next]', 50, 200)
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 250)
    def onEnter(self):
        engine.soundManager.playMusicFade('solace')
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            sm.push(FadeTransitionScene([self], [PlayerSelectScene()]))
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
    def update(self, sm, inputStream):
        self.enter.update(inputStream)
        self.esc.update(inputStream)
    def draw(self, sm, screen):
        # background
        screen.fill(engine.DARK_GREY)
        utils.drawText(screen, 'Main Menu', 50, 50, engine.WHITE, 255)
        self.enter.draw(screen)
        self.esc.draw(screen)

class LevelSelectScene(engine.Scene):
    def __init__(self):
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 300)
    def onEnter(self):
        engine.soundManager.playMusicFade('solace')
    def update(self, sm, inputStream):
        self.esc.update(inputStream)
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_a):
            globals.curentLevel = max(globals.curentLevel-1, 1)
        if inputStream.keyboard.isKeyPressed(pygame.K_d):
            globals.curentLevel = min(globals.curentLevel+1, globals.lastCompletedLevel)
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            # keep players in a sensible order (mainly for cameras)
            utils.orderPlayers()
            # resize player cameras, depending on the number playing
            utils.setPlayerCameras()
            level.loadLevel(globals.curentLevel)
            sm.push(FadeTransitionScene([self], [GameScene()]))

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
    def draw(self, sm, screen):
        # background
        screen.fill(engine.DARK_GREY)
        utils.drawText(screen, 'Level Select', 50, 50, engine.WHITE, 255)
        self.esc.draw(screen)

        # draw level select menu
        for levelNumber in range(1, globals.maxLevel+1):
            c = engine.WHITE
            if levelNumber == globals.curentLevel:
                c = engine.GREEN
            a = 255
            if levelNumber > globals.lastCompletedLevel:
                a = 100
            utils.drawText(screen, str(levelNumber), levelNumber*100, 100, c, a)

class PlayerSelectScene(engine.Scene):
    def __init__(self):
        self.enter = ui.ButtonUI(pygame.K_RETURN, '[Enter=next]', 50, 200)
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 250)
    def onEnter(self):
        engine.soundManager.playMusicFade('solace')
    def update(self, sm, inputStream):
        self.esc.update(inputStream)
        self.enter.update(inputStream)
    def input(self, sm, inputStream):

        # handle each player
        for player in [globals.player1, globals.player2, globals.player3, globals.player4]:

            # add to the game
            if inputStream.keyboard.isKeyPressed(player.input.b1):
                if player not in globals.players:
                    globals.players.append(player)
            
            # remove from the game
            if inputStream.keyboard.isKeyPressed(player.input.b2):
                if player in globals.players:
                    globals.players.remove(player)

        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            if len(globals.players) > 0:
                sm.push(FadeTransitionScene([self], [LevelSelectScene()]))

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
    def draw(self, sm, screen):
        # background
        screen.fill(engine.DARK_GREY)
        utils.drawText(screen, 'Player Select', 50, 50, engine.WHITE, 255)

        self.esc.draw(screen)
        self.enter.draw(screen)

        # draw active players

        if globals.player1 in globals.players:
            screen.blit(utils.playing, (100,100))
        else:
            screen.blit(utils.not_playing, (100,100))
        
        if globals.player2 in globals.players:
            screen.blit(utils.playing, (150,100))
        else:
            screen.blit(utils.not_playing, (150,100))

        if globals.player3 in globals.players:
            screen.blit(utils.playing, (200,100))
        else:
            screen.blit(utils.not_playing, (200,100))

        if globals.player4 in globals.players:
            screen.blit(utils.playing, (250,100))
        else:
            screen.blit(utils.not_playing, (250,100))
        
class GameScene(engine.Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
        self.collectionSystem = gamesystems.CollectionSystem()
        self.battleSystem = gamesystems.BattleSystem()
        self.inputSystem = engine.InputSystem()
        self.physicsSystem = engine.PhysicsSystem()
        self.animationSystem = engine.AnimationSystem()
        self.powerupSystem = gamesystems.PowerupSystem()
        self.traumaSystem = engine.TraumaSystem()
    def onEnter(self):
        engine.soundManager.playMusicFade('dawn')
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_1):
            globals.player1.trauma = 1 #min(1, globals.player1.trauma + 0.2)
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
        if globals.world.isWon():
            # update the level select map accessible levels
            nextLevel = min(globals.curentLevel+1, globals.maxLevel)
            levelToUnlock = max(nextLevel, globals.lastCompletedLevel)
            globals.lastCompletedLevel = levelToUnlock
            globals.curentLevel = nextLevel
            sm.push(WinScene())
        if globals.world.isLost():
            sm.push(LoseScene())
    def update(self, sm, inputStream):
        self.inputSystem.update(inputStream=inputStream)
        self.collectionSystem.update()
        self.battleSystem.update()
        self.physicsSystem.update()
        self.animationSystem.update()
        self.powerupSystem.update()
        self.traumaSystem.update()
    def draw(self, sm, screen):
        # background
        screen.fill(engine.BLACK)
        self.cameraSystem.update(screen)

class WinScene(engine.Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 200)
    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])
    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # draw a transparent bg
        bgSurf = pygame.Surface(pygame.display.get_surface().get_size())
        bgSurf.fill((engine.BLACK))
        utils.blit_alpha(screen, bgSurf, (0,0), self.alpha * 0.7)

        utils.drawText(screen, 'You win!', 50, 50, engine.WHITE, self.alpha)
        self.esc.draw(screen, alpha=self.alpha)

class LoseScene(engine.Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 200)
    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])
    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # draw a transparent bg
        bgSurf = pygame.Surface(pygame.display.get_surface().get_size())
        bgSurf.fill((engine.BLACK))
        utils.blit_alpha(screen, bgSurf, (0,0), self.alpha * 0.7)

        utils.drawText(screen, 'You lose!', 150, 150, engine.WHITE, self.alpha)
        self.esc.draw(screen, alpha=self.alpha)

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

