import engine

#
# create a main scene
#

class MainScene(engine.Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
        self.animationSystem = engine.AnimationSystem()
    def update(self):
        self.animationSystem.update()
    def draw(self):
        self.cameraSystem.update()

mainScene = MainScene()

#
# add some resources
#

engine.resourceManager.addImage('heart', 'images/heart.png')

engine.resourceManager.addImage('player_idle_1', 'images/player/vita_00.png')
engine.resourceManager.addImage('player_idle_2', 'images/player/vita_01.png')
engine.resourceManager.addImage('player_idle_3', 'images/player/vita_02.png')
engine.resourceManager.addImage('player_idle_4', 'images/player/vita_03.png')

#
# create a heart entity
#

heartEntity = engine.Entity(
    engine.Position(100, 100, 27, 30)
)
heartImage = engine.ImageGroup(engine.resourceManager.getImage('heart'))
heartEntity.getComponent('imagegroups').add('idle', heartImage)

#
# create an animated player
#

playerEntity = engine.Entity(
    engine.Position(300, 100, 45, 51)
)
playerAnimation = engine.ImageGroup(
        engine.resourceManager.getImage('player_idle_1'),
        engine.resourceManager.getImage('player_idle_2'),
        engine.resourceManager.getImage('player_idle_3'),
        engine.resourceManager.getImage('player_idle_4')
    )
playerEntity.getComponent('imagegroups').add('idle', playerAnimation)

#
# create a camera
#

cameraEntity = engine.Entity(
    engine.CameraComponent(0, 0, 600, 400, bgColour=engine.BLUE)
)
cameraEntity.getComponent('camera').setPosition(300, 200)

#
# add entities to world
#

engine.world.entities.append(heartEntity)
engine.world.entities.append(playerEntity)
engine.world.entities.append(cameraEntity)

#
# add scene to the engine and start
#

engine.init((600, 400), caption='Engine // Image and Animation Example')
engine.sceneManager.push(mainScene)
engine.run()