import pygame
import globals
import utils

class Level:
    def __init__(self, platforms=None, entities=None, winFunc=None, loseFunc=None, powerupSpawnPoints=None):
        self.platforms = platforms
        self.entities = entities
        self.winFunc = winFunc
        self.loseFunc = loseFunc
        self.powerupSpawnPoints = powerupSpawnPoints
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
        if entity.type == 'player':
            if entity.battle is not None:
                if entity.battle.lives > 0:
                    return False
    # level is lost otherwise
    return True

# win if no collectable items left
def wonLevel(level):
    # level isn't won if any collectable exists
    for entity in level.entities:
        if entity.type == 'collectable':
            return False
    # level isn't won otherwise
    return True

def loadLevel(levelNumber):
    if levelNumber == 1:
        # load level 1
        globals.world = Level(
            platforms = [
                # middle
                pygame.Rect(100,300,400,50),
                # left
                pygame.Rect(100,250,50,50),
                # right
                pygame.Rect(450,250,50,50)
            ],
            entities = [
                utils.makeCoin(100,200),
                utils.makeCoin(200,250),
                utils.makeEnemy(150,274)
            ],
            winFunc = wonLevel,
            loseFunc = lostLevel,
            powerupSpawnPoints = [(400,260),(300,100)]
        )
    if levelNumber == 2:
        # load level 2
        globals.world = Level(
            platforms = [
                # middle
                pygame.Rect(100,300,400,50)
            ],
            entities = [
                utils.makeCoin(100,200)
            ],
            winFunc = wonLevel,
            loseFunc = lostLevel,
            powerupSpawnPoints = [(400,260),(300,100)]
        )
     if levelNumber == 3:
            # load level 3
            globals.world = Level(
                platforms=[
                    # middle
                    # reminder rect =left top width height
                    pygame.Rect(100, 300, 400, 50),
                    pygame.Rect(150, 200, 400, 40),
                    pygame.Rect(160, 500, 400, 50)
                #     WARNING  THIS CODE IS BUGGY   FIXXXXX ITTTT ORRR ELSSSEEEEE!!!!!
                #     FIXME: THIS CODE IS BUGGY
                #     ERROR THIS CODE IS EXTREMELY BUGGY FIX IT

                ],
                entities=[
                    utils.makeCoin(100, 200),
                    utils.makeCoin(500, 240),
                    utils.makeCoin(30, 500),
                    utils.makeEnemy(200, 480)
                ],
                winFunc=wonLevel,
                loseFunc=lostLevel,
                powerupSpawnPoints=[(400, 260), (300, 100)]
            )
    if levelNumber == 4:
        # load level 4
        globals.world = Level(
            platforms = [ # TODO: "fix this code... find the rectangle (pygame.Rect... to make the game playable )"
                # middle
                # reminder rect =left top width height
                pygame.Rect(100, 300, 400, 50),
                pygame.Rect(150, 200, 400, 40),
                pygame.Rect(160, 500, 400, 50),
                pygame.Rect(0, 700, 900, 50),
            #  TODO: "add more rectangle dont screw this up again make it playable"

            ],
            entities = [
                utils.makeCoin(100,200),
                utils.makeCoin(500,240),
                utils.makeCoin(30, 500),
                utils.makeCoin(900, 700),
                utils.makeEnemy(200,480),
            ],
            winFunc = wonLevel,
            loseFunc = lostLevel,
            powerupSpawnPoints = [(400,260),(300,100)]
            )
    if levelNumber == 5:
        # load level 5
        globals.world = Level(
            platforms = [ # TODO: "fix this code... find the rectangle (pygame.Rect... to make the game playable )"
                # middle
                # reminder rect =left top width height
                pygame.Rect(100, 300, 400, 50),
                pygame.Rect(150, 200, 400, 40),
                pygame.Rect(160, 500, 400, 50),
                pygame.Rect(0, 700, 900, 50),
                pygame.Rect(900,1000,900,50),
            #  TODO: "add more rectangle dont screw this up again make it playable"

            ],
            entities = [
                utils.makeCoin(100,200),
                utils.makeCoin(500,240),
                utils.makeCoin(30, 500),
                utils.makeCoin(900, 700),
                utils.makeEnemy(200,480),
                utils.makeCoin(1500,998)
            ],
            winFunc = wonLevel,
            loseFunc = lostLevel,
            powerupSpawnPoints = [(400,260),(300,100)]
            )
    if levelNumber == 6:
        # load level 6
        globals.world = Level(
            platforms = [ # TODO: "fix this code... find the rectangle (pygame.Rect... to make the game playable )"
                # middle
                # reminder rect =left top width height
                pygame.Rect(120,200,30,500),
                pygame.Rect(300,300,400,50),
                pygame.Rect(600,500,400,60),

                pygame.Rect(100, 300, 400, 50),
                pygame.Rect(200, 100, 300, 100),
                pygame.Rect(50, 400, 200, 150),

                pygame.Rect(100, 300, 400, 40),
                pygame.Rect(600, 400, 150, 50),
                pygame.Rect(200, 500, 300, 50),
                pygame.Rect(50, 200, 250, 50),
                pygame.Rect(250, 350, 200, 40),
                pygame.Rect(50, 350, 100, 40),
                pygame.Rect(500, 400, 250, 40),

            #  TODO: "add more rectangle dont screw this up again make it playable"

            ],
            entities = [
                utils.makeCoin(500,240),

            ],
            winFunc = wonLevel,
            loseFunc = lostLevel,
            powerupSpawnPoints = [(400,260),(300,100)]
            )
    # add players
    for player in globals.players:
        globals.world.entities.append(player)     

    # reset players
    for entity in globals.world.entities:
        entity.reset(entity)
