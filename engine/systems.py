import pygame
import globals
import utils
from .entity_component_system import *
from .colours import *
import random

class TraumaSystem(System):
    def check(self, entity):
        return entity.trauma is not None
    def updateEntity(self, screen, inputStream, entity):    
        entity.trauma =  max(0, entity.trauma - 0.01 )

class AnimationSystem(System):
    def check(self, entity):
        return entity.imageGroups is not None
    def updateEntity(self, screen, inputStream, entity):    
        entity.imageGroups.animationList[entity.state].update()

class PhysicsSystem(System):
    def check(self, entity):
        return entity.position is not None and entity.rigidBody is not None
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
            int(new_x + entity.rigidBody.rect.x),
            int(entity.position.rect.y+entity.rigidBody.rect.y-1),
            entity.rigidBody.rect.width,
            entity.rigidBody.rect.height)
        
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
            int(entity.position.rect.x+entity.rigidBody.rect.x),
            int(new_y + entity.rigidBody.rect.y),
            entity.rigidBody.rect.width,
            entity.rigidBody.rect.height)
        
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

class InputSystem(System):
    def check(self, entity):
        return entity.input is not None and entity.intention is not None
    def updateEntity(self, screen, inputStream, entity):
        # up = jump
        if inputStream.isDown(entity.input.up):
            entity.intention.jump = True
        else:
            entity.intention.jump = False
        # left = moveLeft
        if inputStream.isDown(entity.input.left):
            entity.intention.moveLeft = True
        else:
            entity.intention.moveLeft = False
        # right = moveRight    
        if inputStream.isDown(entity.input.right):
            entity.intention.moveRight = True
        else:
            entity.intention.moveRight = False
        # b1 = zoom out
        if inputStream.isDown(entity.input.b1):
            entity.intention.zoomOut = True
        else:
            entity.intention.zoomOut = False        
        # b2 = zoom in
        if inputStream.isDown(entity.input.b2):
            entity.intention.zoomIn = True
        else:
            entity.intention.zoomIn = False 

class CameraSystem(System):
    def check(self, entity):
        return entity.camera is not None
    def updateEntity(self, screen, inputStream, entity):

        # set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(clipRect)

        # zoom
        if entity.intention is not None:
            if entity.intention.zoomIn:
                entity.camera.zoomLevel = min(4, entity.camera.zoomLevel+0.01)
            if entity.intention.zoomOut:
                # only zoom out if there's more of the world to see
                newZoomLevel = entity.camera.zoomLevel-0.01
                if (globals.world.size[0] * newZoomLevel >= cameraRect.w) or (globals.world.size[1] * newZoomLevel >= cameraRect.h):
                    entity.camera.zoomLevel = newZoomLevel

        # update camera if tracking an entity
        if entity.camera.entityToTrack is not None:

            trackedEntity = entity.camera.entityToTrack

            currentX = entity.camera.worldX
            currentY = entity.camera.worldY

            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.w/2
            targetY = trackedEntity.position.rect.y + trackedEntity.position.rect.h/2

            entity.camera.setWorldPos((currentX * 0.95) + (targetX * 0.05), (currentY * 0.95) + (targetY * 0.05))

        # calculate offsets
        offsetX = cameraRect.x + cameraRect.w/2 - (entity.camera.worldX * entity.camera.zoomLevel)
        offsetY = cameraRect.y + cameraRect.h/2 - (entity.camera.worldY * entity.camera.zoomLevel)

        angle = 0
        # add camera shake
        if entity.trauma is not None:
            offsetX += (entity.trauma ** 3) * (random.random()*2-1) * 20 * entity.camera.zoomLevel
            offsetY += (entity.trauma ** 3) * (random.random()*2-1) * 20 * entity.camera.zoomLevel
            angle += (entity.trauma ** 3) * (random.random()*2-1) * 30 * entity.camera.zoomLevel

        # fill camera background
        screen.fill(BLACK)

        # draw level background
        if globals.world is not None:
            worldRect = pygame.Rect(
                0 + offsetX,
                0 + offsetY,
                globals.world.size[0] * entity.camera.zoomLevel,
                globals.world.size[1] * entity.camera.zoomLevel)
            pygame.draw.rect(screen, DARK_GREY, worldRect)

        # render platforms
        for p in globals.world.platforms:
            newPosRect = pygame.Rect(
                (p.x * entity.camera.zoomLevel) + offsetX,
                (p.y * entity.camera.zoomLevel) + offsetY,
                p.w * entity.camera.zoomLevel,
                p.h * entity.camera.zoomLevel)
            pygame.draw.rect(screen, MUSTARD, newPosRect)

        # render entities
        for e in globals.world.entities:
            s = e.state
            a = e.imageGroups.animationList[s]
            a.draw(screen,
                (e.position.rect.x * entity.camera.zoomLevel) + offsetX,
                (e.position.rect.y * entity.camera.zoomLevel) + offsetY,
                e.direction == 'left', False, entity.camera.zoomLevel, e.imageGroups.alpha)

            # draw rigidBody component
            #if e.rigidBody is not None:
            #    offsetRect = pygame.Rect(
            #        ( (e.position.rect.x + e.rigidBody.rect.x) * entity.camera.zoomLevel) + offsetX,
            #        ( (e.position.rect.y + e.rigidBody.rect.y) * entity.camera.zoomLevel) + offsetY,
            #        e.rigidBody.rect.w * entity.camera.zoomLevel,
            #        e.rigidBody.rect.h * entity.camera.zoomLevel)
            #    pygame.draw.rect(screen, WHITE, offsetRect)

        # entity HUD

        # score
        if entity.score is not None:
            screen.blit(utils.coin0, (entity.camera.rect.x + 10, entity.camera.rect.y + 10))
            utils.drawText(screen, str(entity.score.score), entity.camera.rect.x + 50, entity.camera.rect.y + 10, WHITE, 255)

        # lives
        if entity.battle is not None:
            for l in range(entity.battle.lives):
                screen.blit(utils.heart_image, (entity.camera.rect.x + 200 + (l*50),entity.camera.rect.y + 10))

        # unset clipping rectangle
        screen.set_clip(None)
