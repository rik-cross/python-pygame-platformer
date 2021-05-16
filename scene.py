from engine import entity
import pygame
import utils
import globals
import engine
import level
import gamesystems

hues = [0, 30, 50, 90, 190, 300]

class MainMenuScene(engine.Scene):

    def __init__(self):

        def loadNext():
            engine.sceneManager.push(FadeTransitionScene([self], [PlayerSelectScene()]))

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

class LevelSelectScene(engine.Scene):
    def __init__(self):
    
        def loadNext():
             # keep players in a sensible order (mainly for cameras)
            utils.orderPlayers()
            # resize player cameras, depending on the number playing
            utils.setPlayerCameras()
            level.loadLevel(globals.curentLevel)
            for entity in globals.world.entities:
                entity.reset(entity)
            engine.sceneManager.push(FadeTransitionScene([self], [GameScene()]))

        def popScene():
            engine.sceneManager.pop()
            engine.sceneManager.push(FadeTransitionScene([self], []))

        self.menu = engine.Menu(1500/2, 650)
        self.menu.addButton(engine.ButtonUI('Start game', actionListener=engine.ActionListener(loadNext)))
        self.menu.addButton(engine.ButtonUI('Back to player select', actionListener=engine.ActionListener(popScene)))

    def onEnter(self):
        engine.soundManager.playMusicFade('solace')
    def update(self, sm, inputStream):
        self.menu.update(inputStream)
    def input(self, sm, inputStream):
        if inputStream.isPressed(engine.keys.a):
            globals.curentLevel = max(globals.curentLevel-1, 1)
        if inputStream.isPressed(engine.keys.d):
            globals.curentLevel = min(globals.curentLevel+1, globals.lastCompletedLevel)
            
    def draw(self, sm, screen):
        # background
        screen.fill(engine.DARK_GREY)

        # draw level select menu
        for levelNumber in range(1, globals.maxLevel+1):
            c = engine.WHITE
            if levelNumber == globals.curentLevel:
                c = engine.GREEN
            a = 255
            if levelNumber > globals.lastCompletedLevel:
                a = 100
            engine.drawText(screen, str(levelNumber), levelNumber*100, 100, c, a)

        self.menu.draw(screen)

class PlayerSelectScene(engine.Scene):
    def __init__(self):

        def pushNextScene():
            if len(globals.players) > 0:
                engine.sceneManager.push(FadeTransitionScene([self], [LevelSelectScene()]))

        def popScene():
            engine.sceneManager.pop()
            #engine.sceneManager.pop()
            engine.sceneManager.push(FadeTransitionScene([self], []))

        self.mainMenu = engine.Menu(1500/2, 650)
        self.mainMenu.addButton(engine.ButtonUI('Choose level', actionListener=engine.ActionListener(pushNextScene)))
        self.mainMenu.addButton(engine.ButtonUI('Back to main menu', actionListener=engine.ActionListener(popScene)))

    def onEnter(self):
        engine.soundManager.playMusicFade('solace')
    def update(self, sm, inputStream):
        for player in [globals.player1, globals.player2, globals.player3, globals.player4]:
            player.imageGroups.animationList['idle'].update()

    def input(self, sm, inputStream):

        self.mainMenu.update(inputStream)

        # handle each player
        for player in [globals.player1, globals.player2, globals.player3, globals.player4]:

            # add to the game
            if inputStream.isPressed(player.input.b1):
                if player not in globals.players:
                    globals.players.append(player)
            
            # remove from the game
            if inputStream.isPressed(player.input.b2):
                if player in globals.players:
                    globals.players.remove(player)
            
            # recolour
            if inputStream.isPressed(player.input.right):
                if player in globals.players:

                    colourClash = True
                    currentHuePos = hues.index(player.imageGroups.hue)
                    nextHuePos = currentHuePos

                    # dont allow two player to be the same colour
                    while colourClash:
                        colourClash = False
                        nextHuePos = (nextHuePos+1)%(len(hues))
                        nextHue = hues[nextHuePos]
                        for otherPlayer in [globals.player1, globals.player2, globals.player3, globals.player4]:
                            if otherPlayer.imageGroups.hue == nextHue:
                                colourClash = True
                    
                    player.imageGroups.hue = nextHue
            
            if inputStream.isPressed(player.input.left):
                if player in globals.players:

                    colourClash = True
                    currentHuePos = hues.index(player.imageGroups.hue)
                    nextHuePos = currentHuePos

                    # dont allow two player to be the same colour
                    while colourClash:
                        colourClash = False
                        nextHuePos = (nextHuePos-1)%(len(hues))
                        nextHue = hues[nextHuePos]
                        for otherPlayer in [globals.player1, globals.player2, globals.player3, globals.player4]:
                            if otherPlayer.imageGroups.hue == nextHue:
                                colourClash = True
                    
                    player.imageGroups.hue = nextHue

    def draw(self, sm, screen):
        # background
        screen.fill(engine.DARK_GREY)

        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        spacing = screenWidth/4

        positions = [(spacing*i)+90 for i in range(4)]
        players = [globals.player1, globals.player2, globals.player3, globals.player4]

        for player in players:
            # draw active players
            colour = pygame.Color(0)
            colour.hsla = (player.imageGroups.hue, 100, 50, 100)
            #utils.changColour
            if player in globals.players:
                #img = utils.playing
                imgGroup = player.imageGroups.animationList['idle']
                imgList = imgGroup.imageList
                index = imgGroup.imageIndex
                img = imgList[index]
            else:
                img = utils.not_playing
            #screen.blit(pygame.transform.scale(utils.player_shadow, (144*2,144*2)), (positions[players.index(player)]-53,200)) 
            screen.blit(pygame.transform.scale(utils.changeColour(img, colour), (45*4,51*4)), (positions[players.index(player)],250))

        self.mainMenu.draw(screen)            


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
        self.particleSystem = engine.ParticleSystem()
        self.emoteSystem = engine.EmoteSystem()
        self.textSystem = engine.TextSystem()
    def onEnter(self):
        engine.soundManager.playMusicFade('dawn')
    def input(self, sm, inputStream):
        if inputStream.isPressed(engine.keys.esc):
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
        self.emoteSystem.update()
        self.textSystem.update()
    def draw(self, sm, screen):
        # background
        screen.fill(engine.BLACK)
        self.cameraSystem.update(screen)
        self.particleSystem.update(screen)

class WinScene(engine.Scene):
    def __init__(self):
        self.alpha = 0

        def back():
            engine.sceneManager.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), PlayerSelectScene(), LevelSelectScene()])])
        
        self.menu = engine.Menu(1500/2, 650)
        self.menu.addButton(engine.ButtonUI('Back', actionListener=engine.ActionListener(back)))

    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.menu.update(inputStream)
    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # draw a transparent bg
        bgSurf = pygame.Surface(pygame.display.get_surface().get_size())
        bgSurf.fill((engine.BLACK))
        utils.blit_alpha(screen, bgSurf, (0,0), self.alpha * 0.7)

        engine.drawText(screen, 'You win!', 50, 50, engine.WHITE, self.alpha)
        self.menu.draw(screen)

class LoseScene(engine.Scene):
    def __init__(self):
        self.alpha = 0
        
        def back():
            engine.sceneManager.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), PlayerSelectScene(), LevelSelectScene()])])
        
        self.menu = engine.Menu(1500/2, 650)
        self.menu.addButton(engine.ButtonUI('Back', actionListener=engine.ActionListener(back)))

    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.menu.update(inputStream)
    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # draw a transparent bg
        bgSurf = pygame.Surface(pygame.display.get_surface().get_size())
        bgSurf.fill((engine.BLACK))
        utils.blit_alpha(screen, bgSurf, (0,0), self.alpha * 0.7)

        engine.drawText(screen, 'You lose!', 150, 150, engine.WHITE, self.alpha)
        self.menu.draw(screen)

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

