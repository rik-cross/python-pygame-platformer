import pygame
import utils
import globals
import random
from .colours import *
from .entity_component_system import *

from .soundmanager import *
from .inputmanager import *
from .scenemanager import *

from .components import *
from .systems import *

sceneManager = SceneManager()
inputManager = InputManager()
soundManager = SoundManager()

clock = pygame.time.Clock()

def init(size, caption):
    global screen
    pygame.init()
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

        #print(inputManager.isReleased(engine.controller[0].switchTest))

        clock.tick(60)

    # quit
    pygame.quit()



