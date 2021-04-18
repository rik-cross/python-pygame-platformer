import engine
import globals
import random
import utils

class PowerupSystem(engine.System):
    def __init__(self):
        self.timer = 0
    def check(self, entity):
        return entity.effect is not None
    def update(self, screen=None, inputStream=None):
        super().update(screen, inputStream)

        # count the number of powerups in the world
        count = 0
        for entity in globals.world.entities:
            if entity.tags.has('player'):
                if entity.effect:
                    count += 1

        # if no powerups -- start a timer to create new
        if count == 0 and self.timer == 0:
            self.timer = 500

        # create new powerup if it's time
        if self.timer > 0:
            # decrement timer
            self.timer -= 1
            if self.timer <= 0:
                # spawn a powerup
                if globals.world.powerupSpawnPoints is not None:
                    if len(globals.world.powerupSpawnPoints) > 0:
                        spawnPos = random.choice(globals.world.powerupSpawnPoints)
                        globals.world.entities.append(
                            utils.makePowerup(random.choice(utils.powerups), spawnPos[0], spawnPos[1])
                        )

    def updateEntity(self, screen, inputStream, entity):

        # player collection of powerups
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.tags.has('player') and not entity.tags.has('player'):
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # give the effect component to the player
                    otherEntity.effect = entity.effect
                    engine.soundManager.playSound(entity.effect.sound)
                    # remove the collected powerup from the world
                    globals.world.entities.remove(entity)
        
        # apply powerup effects for players
        if entity.tags.has('player'):
            entity.effect.apply(entity)
            entity.effect.timer -= 1
            # if the effect has run out
            if entity.effect.timer < 0:
                # reset entity if appropriate
                if entity.effect.end:
                    entity.effect.end(entity)
                # destroy the effect
                entity.effect = None

class CollectionSystem(engine.System):
    def check(self, entity):
        return entity.tags.has('player') and entity.score is not None   
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.tags.has('collectable'):
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # entity.collectable.onCollide(entity, otherEntity)
                    engine.soundManager.playSound('coin')
                    globals.world.entities.remove(otherEntity)
                    entity.score.score += 1

class BattleSystem(engine.System):
    def check(self, entity):
        return entity.tags.has('player') and entity.battle is not None   
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.tags.has('dangerous'):
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # entity.battle.onCollide(entity, otherEntity)
                    entity.battle.lives -= 1
                    
                    # reset player position
                    entity.position.rect.x = entity.position.initial.x
                    entity.position.rect.y = entity.position.initial.y
                    entity.speed = 0

                    # remove player if no lives left
                    if entity.battle.lives <= 0:
                        globals.world.entities.remove(entity)
