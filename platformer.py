import pygame
import engine
import utils
import level
import scene
import globals

# constant variables
SCREEN_SIZE = (830,830)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Rik\'s Platform Game')
clock = pygame.time.Clock()

sceneManager = engine.SceneManager()

mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

inputStream = engine.InputStream()

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

running = True
while running:
# game loop

    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    inputStream.processInput()
    engine.soundManager.update()

    if sceneManager.isEmpty():
        running = False
    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen) 

    clock.tick(60)

# quit
pygame.quit()