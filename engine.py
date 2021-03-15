import pygame
import utils
import globals
import random

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, screen=None, inputStream=None):
        for entity in globals.world.entities:
            if self.check(entity):
                self.updateEntity(screen, inputStream, entity)
    def updateEntity(self, screen, inputStream, entity):
        pass

class PowerupSystem(System):
    def __init__(self):
        self.timer = 0
    def check(self, entity):
        return entity.effect is not None
    def update(self, screen=None, inputStream=None):
        super().update(screen, inputStream)

        # count the number of powerups in the world
        count = 0
        for entity in globals.world.entities:
            if entity.type != 'player':
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

        print('count:', count, 'timer', self.timer)

    def updateEntity(self, screen, inputStream, entity):

        # player collection of powerups
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'player' and entity.type != 'player':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # give the effect component to the player
                    otherEntity.effect = entity.effect
                    globals.soundManager.playSound(entity.effect.sound)
                    # remove the collected powerup from the world
                    globals.world.entities.remove(entity)
        
        # apply powerup effects for players
        if entity.type == 'player':
            entity.effect.apply(entity)
            entity.effect.timer -= 1
            # if the effect has run out
            if entity.effect.timer < 0:
                # reset entity if appropriate
                if entity.effect.end:
                    entity.effect.end(entity)
                # destroy the effect
                entity.effect = None

class AnimationSystem(System):
    def check(self, entity):
        return entity.animations is not None
    def updateEntity(self, screen, inputStream, entity):    
        entity.animations.animationList[entity.state].update()

class PhysicsSystem(System):
    def check(self, entity):
        return entity.position is not None
    def updateEntity(self, screen, inputStream, entity):

        new_x = entity.position.rect.x
        new_y = entity.position.rect.y

        if entity.intention is not None:
            if entity.intention.moveLeft:
                new_x -= 2
                entity.direction = 'left'
                entity.state = 'walking'
            if entity.intention.moveRight:
                new_x += 2
                entity.direction = 'right'
                entity.state = 'walking'
            if not entity.intention.moveLeft and not entity.intention.moveRight:
                entity.state = 'idle'
            if entity.intention.jump and entity.on_ground:
                globals.soundManager.playSound('jump')
                entity.state = 'jumping'
                entity.speed = -5

        # horizontal movement

        new_x_rect = pygame.Rect(
            int(new_x),
            int(entity.position.rect.y-1),
            entity.position.rect.width,
            entity.position.rect.height)
        
        x_collision = False

        #...check against every platform
        for platform in globals.world.platforms:
            if platform.colliderect(new_x_rect):
                x_collision = True
                break

        if x_collision == False:
            entity.position.rect.x = new_x
        
        # vertical movement

        entity.speed += entity.acceleration
        new_y += entity.speed

        new_y_rect = pygame.Rect(
            int(entity.position.rect.x),
            int(new_y),
            entity.position.rect.width,
            entity.position.rect.height)
        
        y_collision = False
        entity.on_ground = False

        #...check against every platform
        for platform in globals.world.platforms:
            if platform.colliderect(new_y_rect):
                y_collision = True
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
        if inputStream.keyboard.isKeyDown(entity.input.up):
            entity.intention.jump = True
        else:
            entity.intention.jump = False
        # left = moveLeft
        if inputStream.keyboard.isKeyDown(entity.input.left):
            entity.intention.moveLeft = True
        else:
            entity.intention.moveLeft = False
        # right = moveRight    
        if inputStream.keyboard.isKeyDown(entity.input.right):
            entity.intention.moveRight = True
        else:
            entity.intention.moveRight = False
        # b1 = zoom out
        if inputStream.keyboard.isKeyDown(entity.input.b1):
            entity.intention.zoomOut = True
        else:
            entity.intention.zoomOut = False        
        # b2 = zoom in
        if inputStream.keyboard.isKeyDown(entity.input.b2):
            entity.intention.zoomIn = True
        else:
            entity.intention.zoomIn = False 

class CollectionSystem(System):
    def check(self, entity):
        return entity.type == 'player' and entity.score is not None   
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'collectable':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # entity.collectable.onCollide(entity, otherEntity)
                    globals.soundManager.playSound('coin')
                    globals.world.entities.remove(otherEntity)
                    entity.score.score += 1

class BattleSystem(System):
    def check(self, entity):
        return entity.type == 'player' and entity.battle is not None   
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'dangerous':
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

class CameraSystem(System):
    def check(self, entity):
        return entity.camera is not None
    def updateEntity(self, screen, inputStream, entity):

        # zoom
        if entity.intention is not None:
            if entity.intention.zoomIn:
                entity.camera.zoomLevel = min(4, entity.camera.zoomLevel+0.01)
            if entity.intention.zoomOut:
                entity.camera.zoomLevel = max(0.1, entity.camera.zoomLevel-0.01)

        # set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(clipRect)

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

        # fill camera background
        screen.fill(globals.BLACK)

        # draw level background
        if globals.world is not None:
            worldRect = pygame.Rect(
                0 + offsetX,
                0 + offsetY,
                globals.world.size[0] * entity.camera.zoomLevel,
                globals.world.size[1] * entity.camera.zoomLevel)
            pygame.draw.rect(screen, (50,50,50), worldRect)

        # render platforms
        for p in globals.world.platforms:
            newPosRect = pygame.Rect(
                (p.x * entity.camera.zoomLevel) + offsetX,
                (p.y * entity.camera.zoomLevel) + offsetY,
                p.w * entity.camera.zoomLevel,
                p.h * entity.camera.zoomLevel)
            pygame.draw.rect(screen, globals.MUSTARD, newPosRect)

        # render entities
        for e in globals.world.entities:
            s = e.state
            a = e.animations.animationList[s]
            a.draw(screen,
                (e.position.rect.x * entity.camera.zoomLevel) + offsetX,
                (e.position.rect.y * entity.camera.zoomLevel) + offsetY,
                e.direction == 'left', False, entity.camera.zoomLevel, e.animations.alpha)

        # entity HUD

        # score
        if entity.score is not None:
            screen.blit(utils.coin0, (entity.camera.rect.x + 10, entity.camera.rect.y + 10))
            utils.drawText(screen, str(entity.score.score), entity.camera.rect.x + 50, entity.camera.rect.y + 10, globals.WHITE, 255)

        # lives
        if entity.battle is not None:
            for l in range(entity.battle.lives):
                screen.blit(utils.heart_image, (entity.camera.rect.x + 200 + (l*50),entity.camera.rect.y + 10))

        # unset clipping rectangle
        screen.set_clip(None)

class Camera:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
        self.zoomLevel = 1
    def setWorldPos(self, x, y):
        newX = x
        newY = y
  
        if globals.world is not None:

            # calculate x value

            # if world narrower than camera:
            if (self.rect.w) > (globals.world.size[0]*self.zoomLevel):
                newX = (globals.world.size[0] / 2)
            else:
                newX = max(newX, (self.rect.w/self.zoomLevel)/2)
                newX = min(newX, ( ((globals.world.size[0]) - (self.rect.w/2/self.zoomLevel)) ) )

            # calculate y value

            # if world narrower than camera:
            if self.rect.h > (globals.world.size[1]*self.zoomLevel):
                newY = (globals.world.size[1] / 2)
            else:
                newY = max(newY, (self.rect.h/self.zoomLevel/2))
                newY = min(newY, ( ((globals.world.size[1]) - (self.rect.h/2/self.zoomLevel)) ) )

        self.worldX = newX
        self.worldY = newY

    def trackEntity(self, e):
        self.entityToTrack = e

class Position():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)
        self.initial = pygame.Rect(x,y,w,h)

class Animations():
    def __init__(self):
        self.animationList = {}
        self.alpha = 255
    def add(self, state, animation):
        self.animationList[state] = animation

class Animation:
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 8
    def update(self):
        # increment the timer
        self.animationTimer += 1
        # if the timer gets too high...
        if self.animationTimer >= self.animationSpeed:
            # reset the timer
            self.animationTimer = 0
            # increment the current image
            self.imageIndex += 1
            # loop back to the first image in the list
            # once the index gets too high
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0
    def draw(self, screen, x, y, flipX, flipY, zoomLevel, alpha):
        image = self.imageList[self.imageIndex]
        image.set_alpha(alpha)
        newWidth = int(image.get_rect().w * zoomLevel)
        newHeight = int(image.get_rect().h * zoomLevel)
        screen.blit(pygame.transform.scale(pygame.transform.flip(image, flipX, flipY), (newWidth, newHeight)), (x, y))

class Score:
    def __init__(self):
        self.score = 0

class Battle:
    def __init__(self):
        self.lives = 3

class Input:
    def __init__(self, up, down, left, right, b1, b2):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.b1 = b1
        self.b2 = b2

class Intention:
    def __init__(self):
        self.moveLeft = False
        self.moveRight = False
        self.jump = False
        self.zoomIn = False
        self.zoomOut = False

class Effect:
    def __init__(self, apply, timer, sound, end):
        self.apply = apply
        self.timer = timer
        self.sound = sound
        self.end = end

def resetEntity(entity):
    pass

class Entity:
    def __init__(self):
        self.state = 'idle'
        self.type = 'normal'
        self.position = None
        self.animations = Animations()
        self.direction = 'right'
        self.camera = None
        self.score = None
        self.battle = None
        self.speed = 0
        self.input = None
        self.intention = None
        self.on_ground = False
        self.acceleration = 0
        self.effect = None
        self.reset = resetEntity

