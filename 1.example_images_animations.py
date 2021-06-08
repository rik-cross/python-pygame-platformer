import engine

#
# Create a simple example game scene
#

im = engine.inputManager

class MainScene(engine.Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
        self.animationSystem = engine.AnimationSystem()
    def update(self, sm, im):
        self.animationSystem.update()
    def draw(self, sm, screen):
        self.cameraSystem.update(screen)

mainGameScene = MainScene()

#
# Add some media assets
#

engine.resourceManager.addImage('heart', 'images/heart.png')

engine.resourceManager.addImage('player_idle_1', 'images/player/vita_00.png')
engine.resourceManager.addImage('player_idle_2', 'images/player/vita_01.png')
engine.resourceManager.addImage('player_idle_3', 'images/player/vita_02.png')
engine.resourceManager.addImage('player_idle_4', 'images/player/vita_03.png')

#
# Create a heart entity
#

heart = engine.Entity(
    engine.Position(100,100,32,32)
)
heartImageGroup = engine.ImageGroup( [engine.resourceManager.getImage('heart')] )
heart.getComponent('imagegroups').add('idle', heartImageGroup)

#
# Create an animated player
#

player = engine.Entity(
    engine.Position(300,100,45,51)
)
playerAnimation = engine.ImageGroup( [
        engine.resourceManager.getImage('player_idle_1'),
        engine.resourceManager.getImage('player_idle_2'),
        engine.resourceManager.getImage('player_idle_3'),
        engine.resourceManager.getImage('player_idle_4')
    ] )
player.getComponent('imagegroups').add('idle', playerAnimation)

#
# Create a camera
#

camera = engine.Entity(
    engine.CameraComponent(0,0,600,400)
)
camera.getComponent('camera').setWorldPos(300,200)

#
# Add entities to world
#

engine.world.entities.append(heart)
engine.world.entities.append(player)
engine.world.entities.append(camera)

#
# Add scene to the engine and start
#

engine.init((600,400), caption='Engine // Image and Animation Example')
engine.sceneManager.push(mainGameScene)
engine.run()