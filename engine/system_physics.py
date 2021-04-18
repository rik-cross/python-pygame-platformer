import pygame
import globals
import utils
from .system import *
from .colours import *
import random

class PhysicsSystem(System):
    def check(self, entity):
        return entity.position is not None and entity.collider is not None
    def updateEntity(self, screen, inputStream, entity):

        #
        # use the entity intentions to update the transform component
        #

        # vertical transform

        if entity.intention is not None:
            if entity.intention.jump and entity.on_ground:
                engine.soundManager.playSound('jump')
                entity.state = 'jumping'
                entity.motion.velocity.y = -7

        entity.motion.velocity.y += entity.motion.acceleration.y
        entity.transform.position.y = entity.position.rect.y + entity.motion.velocity.y

        # horizontal transform

        entity.transform.position.x = entity.position.rect.x

        if entity.intention is not None:
            if entity.intention.moveLeft:
                entity.transform.position.x -= 3
                entity.direction = 'left'
                entity.state = 'walking'
            if entity.intention.moveRight:
                entity.transform.position.x += 3
                entity.direction = 'right'
                entity.state = 'walking'
            if not entity.intention.moveLeft and not entity.intention.moveRight:
                entity.state = 'idle'

        #
        # use the transform component to check for and resolve collisions
        #

        # vertical collisions

        new_y_rect = pygame.Rect(
            int(entity.position.rect.x+entity.collider.rect.x),
            int(entity.transform.position.y + entity.collider.rect.y),
            entity.collider.rect.width,
            entity.collider.rect.height)
        
        y_collision = False
        entity.on_ground = False

        #...check against every platform
        for platform in globals.world.platforms:
            if platform.colliderect(new_y_rect):
                y_collision = True
                if abs(entity.motion.velocity.y) > 10:
                    entity.trauma += 0.5

                entity.motion.velocity.y = 0
                # if the platform is below the player
                if platform[1] > entity.transform.position.y:
                    # stick the player to the platform
                    entity.position.rect.y = platform[1] - entity.position.rect.height + 1
                    entity.on_ground = True
                break

        if y_collision == False:
            entity.position.rect.y = int(entity.transform.position.y)

        # horizontal collisions
        
        new_x_rect = pygame.Rect(
            int(entity.transform.position.x + entity.collider.rect.x),
            int(entity.position.rect.y+entity.collider.rect.y-1),
            entity.collider.rect.width,
            entity.collider.rect.height)
        
        x_collision = False

        #...check against every platform
        for platform in globals.world.platforms:
            if platform.colliderect(new_x_rect):
                x_collision = True
                if abs(entity.motion.velocity.x) > 10:
                    entity.trauma += 0.5
                break

        if x_collision == False:
            entity.position.rect.x = entity.transform.position.x

        if entity.tags.has('player') and not entity.on_ground:
            entity.state = 'jumping'
        
        # reset intentions
        if entity.intention is not None:
            entity.intention.reset()