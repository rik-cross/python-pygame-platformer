import engine

engine.resourceManager.addImage('tile_dirt', 'images/textures/dirt.png')
engine.resourceManager.addImage('tile_grass', 'images/textures/grass.png')
engine.resourceManager.addImage('tile_water', 'images/textures/water.png')
engine.resourceManager.addImage('tile_spawn', 'images/textures/spawn_point.png')

engine.Tile.addTile('dirt', engine.Tile(engine.resourceManager.getImage('tile_dirt'), True))
engine.Tile.addTile('grass', engine.Tile(engine.resourceManager.getImage('tile_grass'), True))
engine.Tile.addTile('water', engine.Tile(engine.resourceManager.getImage('tile_water'), False))

engine.Tile.addTile('powerup_spawn_point', engine.Tile(engine.resourceManager.getImage('tile_spawn'), False))