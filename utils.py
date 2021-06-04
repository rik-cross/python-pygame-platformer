import pygame
import engine
import globals
import gamecomponents

def changeColour(image, colour):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(colour)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage

# function from:
# https://nerdparadise.com/programming/pygameblitopacity
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

heart_image = pygame.image.load('images/heart.png')

def setHealth(entity):
    if entity.battle:
        entity.battle.lives = 3

def setInvisible(entity):
    if entity.imageGroups:
        entity.imageGroups.alpha = 50

def endInvisible(entity):
    if entity.imageGroups:
        entity.imageGroups.alpha = 255

powerups = ['health', 'invisible']

powerupImages = {
    'health' : [pygame.image.load('images/powerup_health.png')],
    'invisible' : [pygame.image.load('images/powerup_invisible.png')]
}

powerupSound = {
    'health' : 'powerup_get',
    'invisible' : 'powerup_get'
}

powerupApply = {
    'health' : setHealth,
    'invisible' : setInvisible
}

powerupEnd = {
    'health' : None,
    'invisible' : endInvisible
}

powerupEffectTimer = {
    'health' : 0,
    'invisible' : 1000
}

def makePowerup(type, x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,32,32)
    entity.addComponent(engine.Position(x,y,32,32))
    entityAnimation = engine.ImageGroup(powerupImages[type])
    entity.imageGroups.add('idle', entityAnimation)
    entity.getComponent('imagegroups').add('idle', entityAnimation)
    entity.effect = gamecomponents.Effect(
        powerupApply[type], 
        powerupEffectTimer[type],
        powerupSound[type],
        powerupEnd[type]
    )
    entity.addComponent(
        gamecomponents.Effect(
            powerupApply[type], 
            powerupEffectTimer[type],
            powerupSound[type],
            powerupEnd[type]
        )
    )
    entity.tags.add('powerup')
    entity.getComponent('tags').add('powerup')
    return entity    

coin0 = pygame.image.load('images/coin/coin_0.png')
coin1 = pygame.image.load('images/coin/coin_1.png')
coin2 = pygame.image.load('images/coin/coin_2.png')
coin3 = pygame.image.load('images/coin/coin_3.png')
coin4 = pygame.image.load('images/coin/coin_4.png')
coin5 = pygame.image.load('images/coin/coin_5.png')

def makeCoin(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,23,23)
    entityAnimation = engine.ImageGroup([coin1, coin2, coin3, coin4, coin5], delay=12)
    entity.imageGroups.add('idle', entityAnimation)
    entity.tags.add('collectable')
    return entity

sign = pygame.image.load('images/sign.png')

def makeSign(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,50,55)
    entityAnimation = engine.ImageGroup([sign])
    entity.imageGroups.add('idle', entityAnimation)

    entity.triggers = engine.Triggers()
    signTrigger = engine.SignPlayerTrigger(boundingBox = pygame.rect.Rect(0,0,50,55))
    entity.triggers.triggerList.append(signTrigger)
    
    return entity

enemy0 = pygame.image.load('images/spike_monster.png')

def makeEnemy(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,50,26)
    entityAnimation = engine.ImageGroup([enemy0])
    entity.imageGroups.add('idle', entityAnimation)
    entity.tags.add('dangerous')
    return entity

playing = pygame.image.load('images/player/playing.png')
not_playing = pygame.image.load('images/player/not_playing.png')

player_shadow = pygame.image.load('images/player/shadow.png')

idle0 = pygame.image.load('images/player/vita_00.png')
idle1 = pygame.image.load('images/player/vita_01.png')
idle2 = pygame.image.load('images/player/vita_02.png')
idle3 = pygame.image.load('images/player/vita_03.png')

walking0 = pygame.image.load('images/player/vita_04.png')
walking1 = pygame.image.load('images/player/vita_05.png')
walking2 = pygame.image.load('images/player/vita_06.png')
walking3 = pygame.image.load('images/player/vita_07.png')
walking4 = pygame.image.load('images/player/vita_08.png')
walking5 = pygame.image.load('images/player/vita_09.png')

jumping = pygame.image.load('images/player/vita_11.png')

def orderPlayers():
    newPlayerOrder = []
    for player in [globals.player1, globals.player2, globals.player3, globals.player4]:
        if player in globals.players:
            newPlayerOrder.append(player)
    globals.players = newPlayerOrder

def setPlayerCameras():

    screenWidth, screenHeight = pygame.display.get_surface().get_size()

    # 1 player game
    if len(globals.players) == 1:
        cameraWidth = screenWidth - (2*10)
        cameraHeight = screenHeight - (2*10)
        p = globals.players[0]
        p.camera = engine.CameraComponent(10,10,cameraWidth, cameraHeight)
        p.camera.setWorldPos(p.position.initialRect.x, p.position.initialRect.y)
        p.camera.trackEntity(p)
    
    # 2 player game
    if len(globals.players) == 2:

        cameraWidth = (screenWidth - (3*10)) / 2
        cameraHeight = screenHeight - (2*10)

        p1 = globals.players[0]
        p1.camera = engine.CameraComponent(10,10,cameraWidth, cameraHeight)
        p1.camera.setWorldPos(p1.position.initialRect.x, p1.position.initialRect.y)
        p1.camera.trackEntity(p1)

        p2 = globals.players[1]
        p2.camera = engine.CameraComponent((2*10)+cameraWidth,10,cameraWidth, cameraHeight)
        p2.camera.setWorldPos(p2.position.initialRect.x, p2.position.initialRect.y)
        p2.camera.trackEntity(p2)

    # 3 or 4 player game
    if len(globals.players) >= 3:
        cameraWidth = (screenWidth - (3*10)) / 2
        cameraHeight = (screenHeight - (3*10)) / 2
        p1 = globals.players[0]
        p1.camera = engine.CameraComponent(10,10,cameraWidth, cameraHeight)
        p1.camera.setWorldPos(p1.position.initialRect.x, p1.position.initialRect.y)
        p1.camera.trackEntity(p1)

        p2 = globals.players[1]
        p2.camera = engine.CameraComponent((2*10)+cameraWidth,10,cameraWidth, cameraHeight)
        p2.camera.setWorldPos(p2.position.initialRect.x, p2.position.initialRect.y)
        p2.camera.trackEntity(p2)

        p3 = globals.players[2]
        p3.camera = engine.CameraComponent(10,(2*10)+cameraHeight,cameraWidth, cameraHeight)
        p3.camera.setWorldPos(p3.position.initialRect.x, p3.position.initialRect.y)
        p3.camera.trackEntity(p3)

        if len(globals.players) == 4:
            p4 = globals.players[3]
            p4.camera = engine.CameraComponent((2*10)+cameraWidth,(2*10)+cameraHeight,cameraWidth, cameraHeight)
            p4.camera.setWorldPos(p4.position.initialRect.x, p4.position.initialRect.y)
            p4.camera.trackEntity(p4)

def resetPlayer(entity):
    entity.score.score = 0
    entity.battle.lives = 3
    entity.position.reset()
    entity.speed = 0
    entity.velocity = pygame.math.Vector2()
    entity.acceleration = entity.initialAcceleration
    entity.camera.setWorldPos(entity.position.initialRect.x, entity.position.initialRect.y)
    entity.direction = 'right'
    entity.imageGroups.alpha = 255
    entity.effect = None
    entity.state = 'idle'
    if entity.camera is not None:
        entity.camera.zoomLevel = 1
    if entity.transform is not None:
        entity.transform.reset()
    if entity.motion is not None:
        entity.motion.reset()

def playerInput(inputStream, entity):
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
    # down = balloon
    if inputStream.isPressed(entity.input.down):
        entity.intention.fire = True
    else:
        entity.intention.fire = False
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

def makePlayer(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,45,51)
    entityIdleAnimation = engine.ImageGroup([idle0, idle1, idle2, idle3])
    entityWalkingAnimation = engine.ImageGroup([walking0, walking1, walking2, walking3, walking4, walking5], delay=6)
    entityJumpingAnimation = engine.ImageGroup([jumping])
    entity.imageGroups.add('idle', entityIdleAnimation)
    entity.imageGroups.add('walking', entityWalkingAnimation)
    entity.imageGroups.add('jumping', entityJumpingAnimation)
    entity.score = gamecomponents.Score()
    entity.battle = gamecomponents.Battle()
    entity.intention = engine.Intention()
    entity.acceleration = 0.3
    entity.initialAcceleration = entity.acceleration
    entity.reset = resetPlayer
    entity.collider = engine.Collider(10,1,25,50)
    entity.tags.add('player')
    entity.motion = engine.Motion(acceleration=pygame.math.Vector2(0,0.3))
    return entity

def makeCollision(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,1,1)
    entity.particle_emitter = engine.ParticleEmitter()
    entity.imageGroups = None
    return entity

def makeExplosion(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,1,1)
    entity.particle_emitter = engine.ParticleEmitter(size=40, colour=engine.colours.BLUE)
    entity.imageGroups = None
    return entity

balloon = pygame.image.load('images/balloon.png')

def makeBalloon(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,16,16)
    entityIdleImage = engine.ImageGroup([balloon])
    entity.imageGroups.add('idle', entityIdleImage)
    entity.acceleration = 0.3
    entity.initialAcceleration = entity.acceleration
    entity.collider = engine.Collider(2,2,12,12)
    entity.tags.add('balloon')
    entity.motion = engine.Motion(acceleration=pygame.math.Vector2(0,0.3))
    return entity