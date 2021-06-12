from engine.component_imagegroup import ImageGroup
import pygame

from .soundmanager import *
from .inputmanager import *
from .scenemanager import *
from .resourcemanager import *

from .system import System

from .system_animation import *
from .system_camera import *
from .system_emote import *
from .system_input import *
from .system_particle import *
from .system_physics import *
from .system_text import *
from .system_trauma import *
from .system_trigger import *

from .entity_factory import *

from .world import *

pygame.init()

sceneManager = SceneManager()
inputManager = InputManager()

soundManager = SoundManager()
resourceManager = ResourceManager()

# add core game systems
System.addSystem(AnimationSystem())
System.addSystem(EmoteSystem())
System.addSystem(InputSystem())
System.addSystem(PhysicsSystem())
System.addSystem(TextSystem())
System.addSystem(TraumaSystem())
System.addSystem(TriggerSystem())
System.addSystem(ParticleSystem())
System.addSystem(CameraSystem())

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
        sceneManager.input()
        sceneManager.update()
        sceneManager.draw() 

        for s in System.systems:
            s.update()

        #print(clock.get_fps())
        clock.tick(60)

    # quit
    pygame.quit()



