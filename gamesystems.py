import engine
import globals
import random
import utils
import pygame

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
        
         # throwing balloons

        if entity.intention is not None:
            if entity.intention.fire == True:

                # point in the right direction
                if entity.direction == 'right':
                    xx = entity.position.rect.x + 20 + entity.position.rect.w
                    yy = entity.position.rect.y + entity.position.rect.h // 2
                    aa = engine.Motion(velocity=pygame.math.Vector2(4,-6), acceleration=pygame.math.Vector2(0,0.3))
                elif entity.direction == 'left':
                    xx = entity.position.rect.x - 20
                    yy = entity.position.rect.y + entity.position.rect.h // 2
                    aa = engine.Motion(velocity=pygame.math.Vector2(-4,-6), acceleration=pygame.math.Vector2(0,0.3))
                balloon = engine.entityFactory.create('balloon', xx, yy)
                balloon.motion = aa
                balloon.owner = entity
                globals.world.entities.append(balloon)

        # balloon collision
        for otherEntity in globals.world.entities:

            # against other players
            if otherEntity is not entity and entity.tags.has('player') and otherEntity.tags.has('balloon'):
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    globals.world.entities.append(engine.entityFactory.create('explosion', otherEntity.position.rect.x, otherEntity.position.rect.y))
                    engine.soundManager.playSound('explosion', engine.soundManager.soundVolume / 2)
                    explosion_direction = 1
                    if otherEntity.motion.velocity.x < 0:
                        explosion_direction = -1
                    entity.motion.velocity += pygame.math.Vector2(7 * explosion_direction,-7)
                    globals.world.entities.remove(otherEntity)


        # static enemies

        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.tags.has('dangerous'):
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # entity.battle.onCollide(entity, otherEntity)
                    entity.battle.lives -= 1
                    
                    if entity.motion is not None:
                        entity.motion.reset()
                    
                    entity.motion.velocity.y = -2

                    # reset player position
                    if entity.transform is not None:
                        entity.transform.reset()
                    entity.position.rect.x = entity.position.initial.x
                    entity.position.rect.y = entity.position.initial.y
                    # TODO -- should this be in the physics system?
                    entity.speed = 0
                

                    # remove player if no lives left
                    if entity.battle.lives <= 0:
                        globals.world.entities.remove(entity)
