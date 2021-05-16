import pygame
import engine

engine.Tile.addTile('dirt', engine.Tile(pygame.image.load('images/textures/dirt.png'), True))
engine.Tile.addTile('grass', engine.Tile(pygame.image.load('images/textures/grass.png'), True))
engine.Tile.addTile('water', engine.Tile(pygame.image.load('images/textures/water.png'), False))

engine.Tile.addTile('powerup_spawn_point', engine.Tile(pygame.image.load('images/textures/spawn_point.png'), False))