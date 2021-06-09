import engine

#
# Create a main scene
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
# Add some resources
#

engine.resourceManager.addImage('heart', 'images/heart.png')

engine.resourceManager.addImage('player_idle_1', 'images/player/vita_00.png')
engine.resourceManager.addImage('player_idle_2', 'images/player/vita_01.png')
engine.resourceManager.addImage('player_idle_3', 'images/player/vita_02.png')
engine.resourceManager.addImage('player_idle_4', 'images/player/vita_03.png')

#
# Create a heart entity
#

heartEntity = engine.Entity(
    engine.Position(100, 200, 27, 30)
)
heartImage = engine.ImageGroup(engine.resourceManager.getImage('heart'))
heartEntity.getComponent('imagegroups').add('idle', heartImage)

#
# Create an animated player
#

playerEntity = engine.Entity(
    engine.Position(250, 200, 45, 51)
)
playerAnimation = engine.ImageGroup(
        engine.resourceManager.getImage('player_idle_1'),
        engine.resourceManager.getImage('player_idle_2'),
        engine.resourceManager.getImage('player_idle_3'),
        engine.resourceManager.getImage('player_idle_4')
    )
playerEntity.getComponent('imagegroups').add('idle', playerAnimation)

#
# Create some cameras
#

worldCameraEntity = engine.Entity(
    engine.CameraComponent(0, 0, 400, 400, bgColour=engine.BLUE)
)
worldCameraEntity.getComponent('camera').setPosition(200, 200)

heartCameraEntity = engine.Entity(
    engine.CameraComponent(400, 0, 200, 200, bgColour=engine.RED)
)
heartCameraEntity.getComponent('camera').goToEntity(heartEntity)
heartCameraEntity.getComponent('camera').setZoom(5, duration=300)

playerCameraEntity = engine.Entity(
    engine.CameraComponent(400, 200, 200, 200,bgColour=engine.GREEN)
)
playerCameraEntity.getComponent('camera').trackEntity(playerEntity)
playerCameraEntity.getComponent('camera').setZoom(3)

#
# Add entities to world
#

engine.world.entities.append(heartEntity)
engine.world.entities.append(playerEntity)

engine.world.entities.append(worldCameraEntity)
engine.world.entities.append(heartCameraEntity)
engine.world.entities.append(playerCameraEntity)


#
# Add scene to the engine and start
#

engine.init((600, 400), caption='Engine // Camera Example')
engine.sceneManager.push(mainScene)
engine.run()