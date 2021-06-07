from engine import entity
import pygame
import utils
import globals
import engine
import level
import gamesystems
import scene_level_select
import scene_fade_transition

hues = [0, 30, 50, 90, 190, 300]

class PlayerSelectScene(engine.Scene):
    def __init__(self):

        def pushNextScene():
            if len(globals.players) > 0:
                engine.sceneManager.push(scene_fade_transition.FadeTransitionScene([self], [scene_level_select.LevelSelectScene()]))

        def popScene():
            engine.sceneManager.pop()
            engine.sceneManager.push(scene_fade_transition.FadeTransitionScene([self], []))

        self.mainMenu = engine.Menu(1500/2, 650)
        self.mainMenu.addButton(engine.ButtonUI('Choose level', actionListener=engine.ActionListener(pushNextScene)))
        self.mainMenu.addButton(engine.ButtonUI('Back to main menu', actionListener=engine.ActionListener(popScene)))

    def onEnter(self):
        engine.soundManager.playMusicFade('solace')
    def update(self, sm, inputStream):
        for player in [globals.player1, globals.player2, globals.player3, globals.player4]:
            player.getComponent('imagegroups').animationList['idle'].update()

    def input(self, sm, inputStream):

        self.mainMenu.update(inputStream)

        # handle each player
        for player in [globals.player1, globals.player2, globals.player3, globals.player4]:

            # add to the game
            if inputStream.isPressed(player.getComponent('input').b1):
                if player not in globals.players:
                    globals.players.append(player)
            
            # remove from the game
            if inputStream.isPressed(player.getComponent('input').b2):
                if player in globals.players:
                    globals.players.remove(player)
            
            # recolour
            if inputStream.isPressed(player.getComponent('input').right):
                if player in globals.players:

                    colourClash = True
                    currentHuePos = hues.index(player.getComponent('imagegroups').hue)
                    nextHuePos = currentHuePos

                    # dont allow two player to be the same colour
                    while colourClash:
                        colourClash = False
                        nextHuePos = (nextHuePos+1)%(len(hues))
                        nextHue = hues[nextHuePos]
                        for otherPlayer in [globals.player1, globals.player2, globals.player3, globals.player4]:
                            if otherPlayer.getComponent('imagegroups').hue == nextHue:
                                colourClash = True
                    
                    player.getComponent('imagegroups').hue = nextHue
            
            if inputStream.isPressed(player.getComponent('input').left):
                if player in globals.players:

                    colourClash = True
                    currentHuePos = hues.index(player.getComponent('imagegroups').hue)
                    nextHuePos = currentHuePos

                    # dont allow two player to be the same colour
                    while colourClash:
                        colourClash = False
                        nextHuePos = (nextHuePos-1)%(len(hues))
                        nextHue = hues[nextHuePos]
                        for otherPlayer in [globals.player1, globals.player2, globals.player3, globals.player4]:
                            if otherPlayer.getComponent('imagegroups').hue == nextHue:
                                colourClash = True
                    
                    player.getComponent('imagegroups').hue = nextHue

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
            colour.hsla = (player.getComponent('imagegroups').hue, 100, 50, 100)
            #utils.changColour
            if player in globals.players:
                #img = utils.playing
                imgGroup = player.getComponent('imagegroups').animationList['idle']
                imgList = imgGroup.imageList
                index = imgGroup.imageIndex
                img = imgList[index]
            else:
                img = utils.not_playing
            #screen.blit(pygame.transform.scale(utils.player_shadow, (144*2,144*2)), (positions[players.index(player)]-53,200)) 
            screen.blit(pygame.transform.scale(utils.changeColour(img, colour), (45*4,51*4)), (positions[players.index(player)],250))

        self.mainMenu.draw(screen)            
