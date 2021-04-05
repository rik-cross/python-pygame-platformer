import pygame

from .soundmanager import *
from .inputmanager import *
from .scenemanager import *

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

        #print(clock.get_fps())
        clock.tick(60)

    # quit
    pygame.quit()



