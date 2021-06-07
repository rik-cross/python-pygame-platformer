import pygame

from .soundmanager import *
from .inputmanager import *
from .scenemanager import *
from .resourcemanager import *

from .entity_factory import *

from .world import *

pygame.init()

sceneManager = SceneManager()
inputManager = InputManager()

soundManager = SoundManager()
resourceManager = ResourceManager()

entityFactory = EntityFactory()

world = World()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((600,400))

def init(size, caption=''):
    global screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(caption)

def run():
    running = True
    while running:
    # game loop

        # check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        inputManager.processInput()
        soundManager.update()

        if sceneManager.isEmpty():
            running = False
        sceneManager.input(inputManager)
        sceneManager.update(inputManager)
        sceneManager.draw(screen) 

        #print(clock.get_fps())
        clock.tick(60)

    # quit
    pygame.quit()



