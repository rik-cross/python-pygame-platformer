import pygame

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def _update(self, screen, entities, platforms):
        for entity in entities:
            if self.check(entity):
                self.update(screen, entity, entities, platforms)
    def update(self, screen, entity, entities, platforms):
        pass

MUSTARD = (209,206,25)
BLACK = (0,0,0)

class CameraSystem(System):
    def __init__(self):
        super().__init__()
    def check(self, entity):
        return entity.camera is not None
    def update(self, screen, entity, entities, platforms):

        # set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(clipRect)

        # fill camera background
        screen.fill(BLACK)

        # render platforms
        for p in platforms:
            pygame.draw.rect(screen, MUSTARD, p)

        # render entities
        for e in entities:
            s = e.state
            a = e.animations.animationList[s]
            a.draw(screen, e.position.rect.x, e.position.rect.y, e.direction == 'left', False)

        # unset clipping rectangle
        screen.set_clip(None)

class Camera():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)

class Position():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)

class Animations():
    def __init__(self):
        self.animationList = {}
    def add(self, state, animation):
        self.animationList[state] = animation

class Animation():
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
    def draw(self, screen, x, y, flipX, flipY):
        screen.blit(pygame.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (x, y))

class Entity():
    def __init__(self):
        self.state = 'idle'
        self.type = 'normal'
        self.position = None
        self.animations = Animations()
        self.direction = 'right'
        self.camera = None

