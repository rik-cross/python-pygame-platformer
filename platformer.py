# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# Twitter: @ScissorMarks

# Coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0

# Enemy sprite by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

# Heart sprite by Nicole Marie T
# https://opengameart.org/content/heart-1616

# Music by ArcOfDream
# https://arcofdream.itch.io/monolith-ost

# Sound by Maskedsound
# https://maskedsound.itch.io/8-bit-sfx-pack

import pygame
import engine
import utils
import level
import scene
import globals
import inputstream
import soundmanager

# constant variables
SCREEN_SIZE = (830,830)
DARK_GREY = (50,50,50)
MUSTARD = (209,206,25)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Rik\'s Platform Game')
clock = pygame.time.Clock()

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

inputStream = inputstream.InputStream()

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

running = True
while running:
# game loop

    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    inputStream.processInput()
    globals.soundManager.update()

    if sceneManager.isEmpty():
        running = False
    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen) 

    clock.tick(60)

# quit
pygame.quit()