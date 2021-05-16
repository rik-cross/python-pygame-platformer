import engine
import globals
import pygame

#
# Create a simple example game scene
#

class MainScene(engine.Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
    def draw(self, sm, screen):
        screen.fill(engine.BLUE)
        #self.cameraSystem.update(screen)

mainGameScene = MainScene()

#
# Add some media assets
#

playerImage = pygame.image.load('images/heart.png')

#
# Create an entity
#

player = engine.Entity()
player.position = engine.Position(0,0,32,32)
player.imageGroups.add('idle', engine.ImageGroup([playerImage]))

camera = engine.Entity()
camera.camera = engine.Camera(100,100,1300,600)

# hmmmm
# TODO -- don't use globals file
# instead, have engine.entities, engine.map, etc.

#globals.world
#globals.world.entities = [camera]

#
# Add scene to the engine and start
#

engine.init((1500,800), 'Simple Example')
engine.sceneManager.push(mainGameScene)
engine.run()