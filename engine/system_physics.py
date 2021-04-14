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

        new_x = entity.position.rect.x
        new_y = entity.position.rect.y

        if entity.intention is not None:
            if entity.intention.moveLeft:
                new_x -= 3
                entity.direction = 'left'
                entity.state = 'walking'
            if entity.intention.moveRight:
                new_x += 3
                entity.direction = 'right'
                entity.state = 'walking'
            if not entity.intention.moveLeft and not entity.intention.moveRight:
                entity.state = 'idle'
            if entity.intention.jump and entity.on_ground:
                engine.soundManager.playSound('jump')
                entity.state = 'jumping'
                entity.speed = -7

        # horizontal movement

        new_x_rect = pygame.Rect(
            int(new_x + entity.collider.rect.x),
            int(entity.position.rect.y+entity.collider.rect.y-1),
            entity.collider.rect.width,
            entity.collider.rect.height)
        
        x_collision = False

        #...check against every platform
        for platform in globals.world.platforms:
            if platform.colliderect(new_x_rect):
                x_collision = True
                if abs(entity.speed) > 10:
                    entity.trauma += 0.5
                break

        if x_collision == False:
            entity.position.rect.x = new_x
        
        # vertical movement

        entity.speed += entity.acceleration
        new_y += entity.speed

        new_y_rect = pygame.Rect(
            int(entity.position.rect.x+entity.collider.rect.x),
            int(new_y + entity.collider.rect.y),
            entity.collider.rect.width,
            entity.collider.rect.height)
        
        y_collision = False
        entity.on_ground = False

        #...check against every platform
        for platform in globals.world.platforms:
            if platform.colliderect(new_y_rect):
                y_collision = True
                if abs(entity.speed) > 10:
                    entity.trauma += 0.5
                entity.speed = 0
                # if the platform is below the player
                if platform[1] > new_y:
                    # stick the player to the platform
                    entity.position.rect.y = platform[1] - entity.position.rect.height + 1
                    entity.on_ground = True
                break

        if y_collision == False:
            entity.position.rect.y = int(new_y)
        
        if entity.type == 'player' and not entity.on_ground:
            entity.state = 'jumping'
        
        # reset intentions
        if entity.intention is not None:
            entity.intention.moveLeft = False
            entity.intention.moveRight = False
            entity.intention.jump = False