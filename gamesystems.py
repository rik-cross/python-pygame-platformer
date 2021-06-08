import engine
import globals
import random
import utils
import pygame

class PowerupSystem(engine.System):
    
    def __init__(self):
        self.timer = 0
    
    def check(self, entity):
        return entity.hasComponent('effect') #entity.effect is not None
    
    def update(self, screen=None):
        super().update(screen)

        # count the number of powerups in the world
        count = 0
        for entity in engine.world.entities:
            if entity.getComponent('tags').has('powerup'):
                if entity.hasComponent('entity'): #entity.effect:
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
                        engine.world.entities.append(
                            utils.makePowerup(random.choice(utils.powerups), spawnPos[0], spawnPos[1])
                        )
                        engine.soundManager.playSound('powerup_appear', engine.soundManager.soundVolume / 2)

    def updateEntity(self, screen, entity):

        # player collection of powerups
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.getComponent('tags').has('player') and not entity.getComponent('tags').has('player'):
                ep = entity.getComponent('position')
                op = otherEntity.getComponent('position')
                if ep.rect.colliderect(op.rect):
                    # give the effect component to the player
                    #otherEntity.effect = entity.effect
                    otherEntity.addComponent(entity.getComponent('effect'))
                    engine.soundManager.playSound(entity.effect.sound)
                    # remove the collected powerup from the world
                    engine.world.entities.remove(entity)
        
        # apply powerup effects for players
        if entity.getComponent('tags').has('player'):
            ee = entity.getComponent('effect')
            ee.apply(entity)
            ee.timer -= 1
            # if the effect has run out
            if ee.timer < 0:
                # reset entity if appropriate
                if ee.end:
                    ee.end(entity)
                # destroy the effect
                ee = None

class CollectionSystem(engine.System):
    def check(self, entity):
        return entity.getComponent('tags').has('player') and entity.hasComponent('score') #score is not None   
    def updateEntity(self, screen, entity):
        for otherEntity in engine.world.entities:
            if otherEntity is not entity and otherEntity.getComponent('tags').has('collectable'):
                ep = entity.getComponent('position')
                op = otherEntity.getComponent('position')
                if ep.rect.colliderect(op.rect):
                    # entity.collectable.onCollide(entity, otherEntity)
                    engine.soundManager.playSound('coin')
                    engine.world.entities.remove(otherEntity)
                    entity.getComponent('score').score += 1

class BattleSystem(engine.System):
    def check(self, entity):
        return entity.getComponent('tags').has('player') and entity.hasComponent('battle') #battle is not None   
    def updateEntity(self, screen, entity):
         # throwing balloons

        if entity.hasComponent('intention'): #intention is not None:
            if entity.getComponent('intention').fire == True:

                #if entity.intention.fire == True:

                pos = entity.getComponent('position')

                # point in the right direction
                if entity.direction == 'right':
                    xx = pos.rect.x + 10 + pos.rect.w
                    yy = pos.rect.y + pos.rect.h // 2
                    aa = engine.Motion(velocity=pygame.math.Vector2(4,-6), acceleration=pygame.math.Vector2(0,0.3))
                elif entity.direction == 'left':
                    xx = pos.rect.x - 10 - 16 # 16 = balloon width
                    yy = pos.rect.y + pos.rect.h // 2
                    aa = engine.Motion(velocity=pygame.math.Vector2(-4,-6), acceleration=pygame.math.Vector2(0,0.3))
                balloon = engine.entityFactory.create('balloon', xx, yy)
                balloon.addComponent(aa)
                balloon.owner = entity
                engine.world.entities.append(balloon)

        # balloon collision
        for otherEntity in engine.world.entities:

            # against other players
            if otherEntity is not entity and entity.getComponent('tags').has('player') and otherEntity.getComponent('tags').has('balloon'):
                pos = entity.getComponent('position')
                opos = otherEntity.getComponent('position')
                if pos.rect.colliderect(opos.rect):
                    engine.world.entities.append(engine.entityFactory.create('explosion', opos.rect.x, opos.rect.y))
                    engine.soundManager.playSound('explosion', engine.soundManager.soundVolume / 2)
                    explosion_direction = 1
                    if otherEntity.hasComponent('motion'):
                        omot = otherEntity.getComponent('motion')
                        if omot.velocity.x < 0:
                            explosion_direction = -1
                    entity.getComponent('motion').velocity += pygame.math.Vector2(7 * explosion_direction,-7)
                    engine.world.entities.remove(otherEntity)


        # static enemies

        for otherEntity in engine.world.entities:
            if otherEntity is not entity and otherEntity.getComponent('tags').has('dangerous'):

                pos = entity.getComponent('position')
                ops = otherEntity.getComponent('position')

                if pos.rect.colliderect(ops.rect):
                    # entity.battle.onCollide(entity, otherEntity)
                    if entity.hasComponent('battle'):
                        entity.getComponent('battle').lives -= 1
                    
                    if entity.hasComponent('motion'): # motion is not None:
                        entity.getComponent('motion').reset()
                    
                    entity.getComponent('motion').velocity.y = -2

                    # reset player position
                    if entity.hasComponent('transform'): #transform is not None:
                        entity.getComponent('transform').reset()
                    # reset player position
                    pos.reset()
                    # TODO -- should this be in the physics system?
                    entity.speed = 0

                    # remove player if no lives left
                    if entity.getComponent('battle').lives <= 0:
                        engine.world.entities.remove(entity)
