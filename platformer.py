import pygame
import engine
import utils
import level
import scene
import globals

engine.init((1000,500), 'Platform Game')

mainMenu = scene.MainMenuScene()
engine.sceneManager.push(mainMenu)

# create players

# player 1
globals.player1 = utils.makePlayer(300,0)
globals.player1.input = engine.Input(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e)
# player 2
globals.player2 = utils.makePlayer(350,0)
globals.player2.input = engine.Input(pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_u, pygame.K_o)
# player 3
globals.player3 = utils.makePlayer(400,0)
globals.player3.input = engine.Input(pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_x)
# player 4
globals.player4 = utils.makePlayer(450,0)
globals.player4.input = engine.Input(pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_x)

engine.soundManager.addMusic('solace', 'music/23 Solace.ogg')
engine.soundManager.addMusic('dawn', 'music/03 Before the Dawn.ogg')

engine.soundManager.addSound('jump', 'sounds/03_Jump_v2.ogg')
engine.soundManager.addSound('coin', 'sounds/01_Coin Pickup_v2.ogg')


engine.run()