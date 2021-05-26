import engine

#
# Create a simple example game scene
#

im = engine.inputManager

class MainScene(engine.Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
        self.physicsSystem = engine.PhysicsSystem()
    def update(self, sm, im):
        self.physicsSystem.update()
    def draw(self, sm, screen):
        screen.fill(engine.BLUE)
        self.cameraSystem.update(screen)

mainGameScene = MainScene()

#
# Add some media assets
#

engine.imageManager.addImage('player', 'images/heart.png')
engine.imageManager.addImage('grass', 'images/textures/grass.png')
engine.imageManager.addImage('wall', 'images/textures/dirt.png')

#
# Create a tilemap
#

engine.Tile.addTile('grass', engine.Tile(engine.imageManager.getImage('grass'), True))
engine.Tile.addTile('wall', engine.Tile(engine.imageManager.getImage('wall'), True))
engine.world.map = engine.Map(map=[ ['grass' for i in range(16)] for j in range(16) ])
engine.world.map.setTile(8,8,'wall')
engine.world.map.setTile(9,8,'wall')

#
# Create a player entity
#

player = engine.Entity()
player.position = engine.Position(0,0,32,32)
player.imageGroups.add('idle', engine.ImageGroup( [engine.imageManager.getImage('player')] ))

#
# Set camera
#

camera = engine.Entity()
camera.camera = engine.Camera(100,100,1300,600)
center = engine.world.map.getMapCenter()
camera.camera.setWorldPos(center[0],center[1])

#
# Add entities to world
#

engine.world.entities.append(player)
engine.world.entities.append(camera)

#
# Add scene to the engine and start
#

engine.init((1500,800), 'Simple Example')
engine.sceneManager.push(mainGameScene)
engine.run()