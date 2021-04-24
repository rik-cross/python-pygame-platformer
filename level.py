import pygame
import globals
import utils
import engine
import pickle

class Level:
    def __init__(self, size, entities=None, winFunc=None, loseFunc=None, powerupSpawnPoints=None, map=None):
        self.size = size
        self.entities = entities
        self.winFunc = winFunc
        self.loseFunc = loseFunc
        self.powerupSpawnPoints = powerupSpawnPoints
        self.map = map
    def isWon(self):
        if self.winFunc is None:
            return False
        return self.winFunc(self)
    def isLost(self):
        if self.loseFunc is None:
            return False
        return self.loseFunc(self)

# lose if no players have lives remaining
def lostLevel(level):
    # level isn't lost if any player has a life left
    for entity in level.entities:
        if entity.tags.has('player'):
            if entity.battle is not None:
                if entity.battle.lives > 0:
                    return False
    # level is lost otherwise
    return True

# win if no collectable items left
def wonLevel(level):
    # level isn't won if any collectable exists
    for entity in level.entities:
        if entity.tags.has('collectable'):
            return False
    # level isn't won otherwise
    return True

def loadLevel(levelNumber):
    if levelNumber == 1:
        # load level 1
        globals.world = Level(
            size=(40*32, 20*32),
            entities = [
                utils.makeCoin(520,450),
                utils.makeCoin(120,530),
                utils.makeCoin(1700,550),
                utils.makeEnemy(1500,580-26)
            ],
            winFunc = wonLevel,
            loseFunc = lostLevel,
            powerupSpawnPoints = [(900,350),(200,500)],
            map = engine.Map(64,64,'l1')
        )
    if levelNumber == 2:
        # load level 2
        globals.world = Level(
            size=(1200,1200),
            entities = [
                utils.makeCoin(100,200)
            ],
            winFunc = wonLevel,
            loseFunc = lostLevel,
            powerupSpawnPoints = [(400,260),(300,100)],
            map = engine.Map(64,64,'l1')
        )

    # add players
    for player in globals.players:
        globals.world.entities.append(player)     

    # reset players
    for entity in globals.world.entities:
        entity.reset(entity)