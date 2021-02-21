# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# Twitter: @ScissorMarks

# Coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0

# Enemy sprite by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

# Heart sprite by Nicole Marie T
# https://opengameart.org/content/heart-1616

import pygame
import engine
import utils
import level
import scene
import globals
import inputstream

# constant variables
SCREEN_SIZE = (700,500)
DARK_GREY = (50,50,50)
MUSTARD = (209,206,25)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Rik\'s Platform Game')
clock = pygame.time.Clock()

entities = []

coin1 = utils.makeCoin(100,200)
coin2 = utils.makeCoin(200,250)

enemy = utils.makeEnemy(150,274)
enemy.camera = engine.Camera(420,10,200,200)
enemy.camera.setWorldPos(150,250)

player = utils.makePlayer(300,0)
player.camera = engine.Camera(10,10,400,400)
player.camera.setWorldPos(300,0)
player.camera.trackEntity(player)
player.score = engine.Score()
player.battle = engine.Battle()
player.input = engine.Input(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e)
player.intention = engine.Intention()

cameraSys = engine.CameraSystem()

# lose if no players have lives remaining
def lostLevel(level):
    # level isn't lost if any player has a life left
    for entity in level.entities:
        if entity.type == 'player':
            if entity.battle is not None:
                if entity.battle.lives > 0:
                    return False
    # level is lost otherwise
    return True

# win if no collectable items left
def wonLevel(level):
    # level isn't won if any collectable exists
    for entity in level.entities:
        if entity.type == 'collectable':
            return False
    # level isn't won otherwise
    return True

globals.levels[1] = level.Level(
    platforms=[
        # middle
        pygame.Rect(100,300,400,50),
        # left
        pygame.Rect(100,250,50,50),
        # right
        pygame.Rect(450,250,50,50)
    ],
    entities = [
        player, enemy, coin1, coin2
    ],
    winFunc=wonLevel,
    loseFunc=lostLevel
)

globals.levels[2] = level.Level(
    platforms=[
        # middle
        pygame.Rect(100,300,400,50)
    ],
    entities = [
        player, coin1
    ],
    winFunc=wonLevel,
    loseFunc=lostLevel
)

# set the current level
globals.world = globals.levels[1]

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

inputStream = inputstream.InputStream()

running = True
while running:
# game loop

    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    inputStream.processInput()

    if sceneManager.isEmpty():
        running = False
    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen) 

    clock.tick(60)

# quit
pygame.quit()