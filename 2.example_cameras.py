import engine

#
# create a main scene
#

mainScene = engine.Scene()

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
    engine.Position(100, 200, 27, 30)
)
heartImage = engine.ImageGroup(engine.resourceManager.getImage('heart'))
heartEntity.getComponent('imagegroups').add('idle', heartImage)

#
# create an animated player
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
# create some cameras
#

# world camera

worldCameraEntity = engine.Entity(
    engine.CameraComponent(0, 0, 400, 400, bgColour=engine.BLUE)
)
worldCameraEntity.getComponent('camera').setPosition(200, 200)

# heart camera

heartCameraEntity = engine.Entity(
    engine.CameraComponent(400, 0, 200, 200, bgColour=engine.RED)
)
heartCameraEntity.getComponent('camera').goToEntity(heartEntity)
heartCameraEntity.getComponent('camera').setZoom(5, duration=300)

# player camera

playerCameraEntity = engine.Entity(
    engine.CameraComponent(400, 200, 200, 200,bgColour=engine.GREEN)
)
playerCameraEntity.getComponent('camera').trackEntity(playerEntity)
playerCameraEntity.getComponent('camera').setZoom(3)

#
# add entities to world
#

# game entities

engine.world.entities.append(heartEntity)
engine.world.entities.append(playerEntity)

# cameras

engine.world.entities.append(worldCameraEntity)
engine.world.entities.append(heartCameraEntity)
engine.world.entities.append(playerCameraEntity)

#
# add scene to the engine and start
#

engine.init((600, 400), caption='Engine // Camera Example')
engine.sceneManager.push(mainScene)
engine.run()