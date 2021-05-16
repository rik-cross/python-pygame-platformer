import pygame
import globals
import utils
from .system import *
from .colours import *
import random

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
                if (globals.world.map.w_real * newZoomLevel >= cameraRect.w - 10) or (globals.world.map.h_real * newZoomLevel >= cameraRect.h - 10):
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
                globals.world.map.w_real * entity.camera.zoomLevel,
                globals.world.map.h_real * entity.camera.zoomLevel)
            pygame.draw.rect(screen, DARK_GREY, worldRect)

        # render map images behind map
        for img in globals.world.map.mapImages:

            if img.z < 0:

                # there's no parallax for images behind the map

                img.draw(screen,
                    (img.x * entity.camera.zoomLevel) + offsetX,
                    (img.y * entity.camera.zoomLevel) + offsetY,
                    entity.camera.zoomLevel) 

        # render map (to replace platforms)
        if globals.world.map is not None:
            globals.world.map.draw(screen, offsetX, offsetY, entity.camera.zoomLevel)

        # render entities
        for e in globals.world.entities:
            if e.imageGroups is not None:
                s = e.state
                a = e.imageGroups.animationList[s]
                a.draw(screen,
                    (e.position.rect.x * entity.camera.zoomLevel) + offsetX,
                    (e.position.rect.y * entity.camera.zoomLevel) + offsetY,
                    e.direction == 'left', False, entity.camera.zoomLevel, e.imageGroups.alpha, e.imageGroups.hue)

        # render emotes
        for e in globals.world.entities:
            if e.emote is not None:
                eMidPoint = (e.position.rect.w / 2) * entity.camera.zoomLevel
                iMidPoint = (e.emote.image.get_rect().w / 2) * entity.camera.zoomLevel
                xx = e.position.rect.x * entity.camera.zoomLevel + offsetX + eMidPoint - iMidPoint
                
                yy = e.position.rect.y * entity.camera.zoomLevel + offsetY - (e.emote.image.get_rect().h * entity.camera.zoomLevel) - (20 * entity.camera.zoomLevel)
                newWidth = int(e.emote.image.get_rect().w * entity.camera.zoomLevel)
                newHeight = int(e.emote.image.get_rect().h * entity.camera.zoomLevel)
                
                pygame.draw.rect(screen, WHITE, pygame.rect.Rect(xx - (5*entity.camera.zoomLevel), yy - (5*entity.camera.zoomLevel), e.emote.image.get_rect().w * entity.camera.zoomLevel + (10*entity.camera.zoomLevel), e.emote.image.get_rect().h * entity.camera.zoomLevel + (10*entity.camera.zoomLevel)))
                
                bottomOfBox = yy - (5*entity.camera.zoomLevel) + e.emote.image.get_rect().h * entity.camera.zoomLevel + (10*entity.camera.zoomLevel) - 1 
                middleOfBox = e.position.rect.x * entity.camera.zoomLevel + offsetX + eMidPoint
                
                pygame.draw.polygon(screen, WHITE, ((middleOfBox - (10*entity.camera.zoomLevel),bottomOfBox),(middleOfBox + (10*entity.camera.zoomLevel),bottomOfBox),(middleOfBox,bottomOfBox+(10*entity.camera.zoomLevel))))

                screen.blit(pygame.transform.scale(e.emote.image, (newWidth, newHeight)), (xx, yy))

        # render text
        for e in globals.world.entities:
            if e.text is not None:
                e.text.draw(screen, (e.position.rect.x * entity.camera.zoomLevel) + offsetX, (e.position.rect.y * entity.camera.zoomLevel)+ offsetY)

        # particle emitter particles
        for e in globals.world.entities:
            if e.particle_emitter:
                for p in e.particle_emitter.particles:
                    pygame.draw.circle(screen, p.colour, ((p.pos[0]*entity.camera.zoomLevel)+offsetX, (p.pos[1]*entity.camera.zoomLevel)+offsetY), p.size * entity.camera.zoomLevel)

        # render map images infront of map
        for img in globals.world.map.mapImages:

            if img.z >= 0:

                if img.parallaxX:
                    parallaxOffsetX = ((entity.camera.worldX - img.x) * ( (img.z*-1) * 0.2))
                else:
                    parallaxOffsetX = 0
                
                if img.parallaxY:
                    parallaxOffsetY = ((entity.camera.worldY - img.y) * ( (img.z*-1) * 0.2))
                else:
                    parallaxOffsetY = 0

                img.draw(screen,
                    (img.x * entity.camera.zoomLevel) + offsetX + parallaxOffsetX,
                    (img.y * entity.camera.zoomLevel) + offsetY + parallaxOffsetY,
                    entity.camera.zoomLevel)          

        # render text
        for e in globals.world.entities:
            if e.text is not None:
                e.text.draw(screen, (e.position.rect.x * entity.camera.zoomLevel) + offsetX, (e.position.rect.y * entity.camera.zoomLevel)+ offsetY)

        # entity HUD

        # score
        if entity.score is not None:
            screen.blit(utils.coin0, (entity.camera.rect.x + 10, entity.camera.rect.y + 10))
            engine.drawText(screen, str(entity.score.score), entity.camera.rect.x + 50, entity.camera.rect.y + 10, WHITE, 255)

        # lives
        if entity.battle is not None:
            for l in range(entity.battle.lives):
                screen.blit(utils.heart_image, (entity.camera.rect.x + 200 + (l*50),entity.camera.rect.y + 10))

        # unset clipping rectangle
        screen.set_clip(None)

        # update zoom
        if entity.camera.zoomPerFrame != 0:
            entity.camera.zoomLevel += entity.camera.zoomPerFrame
            if abs(entity.camera.zoomLevel - entity.camera.targetZoom) < 0.01 :
                entity.camera.zoomPerFrame = 0
        
        # update position
        # x
        if entity.camera.movementPerFrameX != 0:
            entity.camera.worldX += entity.camera.movementPerFrameX
            if abs(entity.camera.worldX - entity.camera.targetX) < 0.1 :
                entity.camera.movementPerFrameX = 0
        # y
        if entity.camera.movementPerFrameY != 0:
            entity.camera.worldY += entity.camera.movementPerFrameY
            if abs(entity.camera.worldY - entity.camera.targetY) < 0.1 :
                entity.camera.movementPerFrameY = 0



