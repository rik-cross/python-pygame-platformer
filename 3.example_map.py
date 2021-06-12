import engine

#
# create a main scene
#

class MainScene(engine.Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
    def update(self):
        pass
    def draw(self):
        self.cameraSystem.update()

mainScene = MainScene()

#
# add images
#

engine.resourceManager.addImage('tile_dirt', 'images/textures/dirt.png')
engine.resourceManager.addImage('tile_grass', 'images/textures/grass.png')
engine.resourceManager.addImage('tile_water', 'images/textures/water.png')
engine.resourceManager.addImage('tile_spawn', 'images/textures/spawn_point.png')

#
# add some tiles
#

engine.Tile.addTile('dirt', engine.Tile(engine.resourceManager.getImage('tile_dirt'), True))
engine.Tile.addTile('grass', engine.Tile(engine.resourceManager.getImage('tile_grass'), True))
engine.Tile.addTile('water', engine.Tile(engine.resourceManager.getImage('tile_water'), False))

#
# create a map
#

map = engine.Map(map=[
    ['grass','grass','grass'],
    ['grass','water','water'],
    ['grass','dirt','water']
])
engine.map = map

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