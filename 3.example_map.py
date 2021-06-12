import engine

#
# create a main scene
#

mainScene = engine.Scene()

#
# add images
#

engine.resourceManager.addImage('tile_grass', 'images/textures/grass.png')
engine.resourceManager.addImage('tile_water', 'images/textures/water.png')
engine.resourceManager.addImage('tile_spawn', 'images/textures/spawn_point.png')

#
# add some tiles
#

engine.Tile.addTile('grass', engine.Tile(engine.resourceManager.getImage('tile_grass'), True))
engine.Tile.addTile('water', engine.Tile(engine.resourceManager.getImage('tile_water'), False))

#
# create a map
#

map = engine.Map(map=[ ['grass' for i in range(10)] for j in range(10) ])
map.setTile(3,3,'water')
engine.world.map = map

#
# create a camera
#

worldCameraEntity = engine.Entity(
    engine.CameraComponent(0, 0, 600, 400, bgColour=engine.DARK_GREY)
)
worldCameraEntity.getComponent('camera').setPosition(300, 200)

#
# add camera to world
#

engine.world.entities.append(worldCameraEntity)

#
# add scene to the engine and start
#

engine.init((600, 400), caption='Engine // Map Example')
engine.sceneManager.push(mainScene)
engine.run()