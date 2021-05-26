from .system import *
from .engine import *

class TriggerSystem(System):
    def check(self, entity):
        return entity.position is not None and entity.triggers is not None
    def updateEntity(self, screen, inputStream, entity):

        for trigger in entity.triggers.triggerList:

            trigger.last = trigger.current
            trigger.current = []

            if trigger.boundingBox is not None:

                adjustedRect = pygame.rect.Rect(
                    entity.position.rect.x + trigger.boundingBox.x,
                    entity.position.rect.y + trigger.boundingBox.y,
                    trigger.boundingBox.w,
                    trigger.boundingBox.h
                )

                for otherEntity in engine.world.entities:

                    if otherEntity.position is not None and otherEntity.collider is not None:
                        otherRect = pygame.rect.Rect(
                            otherEntity.position.rect.x + otherEntity.collider.rect.x,
                            otherEntity.position.rect.y + otherEntity.collider.rect.y,
                            otherEntity.collider.rect.w,
                            otherEntity.collider.rect.h
                        )

                        if adjustedRect.colliderect(otherRect):
                            trigger.current.append(otherEntity.ID)

                #print(trigger.current)
                
            if trigger.current and not trigger.last:
                trigger.onEnter(entity)
            elif not trigger.current and trigger.last:
                trigger.onExit(entity)
            elif trigger.current:
                trigger.onStay(entity)
            
                #print(world.getEntitiesByTagList(['player1'])[0].ID)
                            #trigger.onCollide(otherEntity)