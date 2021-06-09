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

heart_image = pygame.image.load('images/heart.png')

def setHealth(entity):
    if entity.hasComponent('battle'):
        entity.getComponent('battle').lives = 3

def setInvisible(entity):
    if entity.hasComponent('imagegroups'):
        entity.getComponent('imagegroups').alpha = 50

def endInvisible(entity):
    if entity.hasComponent('imagegroups'):
        entity.imageGroups.alpha = 255

powerups = ['health', 'invisible']

powerupImages = {
    'health' : pygame.image.load('images/powerup_health.png'),
    'invisible' : pygame.image.load('images/powerup_invisible.png')
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
    entity.addComponent(engine.Position(x,y,32,32))
    entityAnimation = engine.ImageGroup(powerupImages[type])
    entity.getComponent('imagegroups').add('idle', entityAnimation)
    entity.addComponent(
        gamecomponents.Effect(
            powerupApply[type], 
            powerupEffectTimer[type],
            powerupSound[type],
            powerupEnd[type]
        )
    )
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
    entityAnimation = engine.ImageGroup(coin1, coin2, coin3, coin4, coin5, delay=12)
    entity.addComponent(engine.Position(x,y,23,23))
    entity.getComponent('imagegroups').add('idle', entityAnimation)
    entity.getComponent('tags').add('collectable')

    return entity

sign = pygame.image.load('images/sign.png')

def makeSign(x,y):
    entity = engine.Entity()
    entityAnimation = engine.ImageGroup(sign)
    signTrigger = engine.SignPlayerTrigger(boundingBox = pygame.rect.Rect(0,0,50,55))
    entity.addComponent(engine.Position(x,y,50,55))
    entity.getComponent('imagegroups').add('idle', entityAnimation)
    entity.addComponent(engine.Triggers())
    entity.getComponent('triggers').triggerList.append(signTrigger)
    return entity

enemy0 = pygame.image.load('images/spike_monster.png')

def makeEnemy(x,y):
    entity = engine.Entity()
    entityAnimation = engine.ImageGroup(enemy0)
    entity.addComponent(engine.Position(x,y,50,26))
    entity.getComponent('imagegroups').add('idle', entityAnimation)
    entity.getComponent('tags').add('dangerous')
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
        p.addComponent(engine.CameraComponent(10,10,cameraWidth, cameraHeight))
        p.getComponent('camera')._updateWorldPos(p.getComponent('position').initialRect.x, p.getComponent('position').initialRect.y)
        p.getComponent('camera').trackEntity(p)
    
    # 2 player game
    if len(globals.players) == 2:

        cameraWidth = (screenWidth - (3*10)) / 2
        cameraHeight = screenHeight - (2*10)

        p1 = globals.players[0]
        p2 = globals.players[1]

        p1.addComponent(engine.CameraComponent(10,10,cameraWidth, cameraHeight))
        p1.getComponent('camera')._updateWorldPos(p1.getComponent('position').initialRect.x, p1.getComponent('position').initialRect.y)
        p1.getComponent('camera').trackEntity(p1)

        p2.addComponent()
        p2.getComponent('camera')._updateWorldPos(p2.getComponent('position').initialRect.x, p2.getComponent('position').initialRect.y)
        p2.getComponent('camera').trackEntity(p2)

    # 3 or 4 player game
    if len(globals.players) >= 3:
        cameraWidth = (screenWidth - (3*10)) / 2
        cameraHeight = (screenHeight - (3*10)) / 2
        p1 = globals.players[0]
        p1.addComponent(engine.CameraComponent(10,10,cameraWidth, cameraHeight))
        p1.getComponent('camera')._updateWorldPos(p1.getComponent('position').initialRect.x, p1.getComponent('position').initialRect.y)
        p1.getComponent('camera').trackEntity(p1)

        p2 = globals.players[1]
        p2.addComponent(engine.CameraComponent((2*10)+cameraWidth,10,cameraWidth, cameraHeight))
        p2.getComponent('camera')._updateWorldPos(p2.getComponent('position').initialRect.x, p2.getComponent('position').initialRect.y)
        p2.getComponent('camera').trackEntity(p2)

        p3 = globals.players[2]
        p3.addComponent(engine.CameraComponent(10,(2*10)+cameraHeight,cameraWidth, cameraHeight))
        p3.getComponent('camera')._updateWorldPos(p3.getComponent('position').initialRect.x, p3.getComponent('position').initialRect.y)
        p3.getComponent('camera').trackEntity(p3)

        if len(globals.players) == 4:
            p4 = globals.players[3]
            p4.addComponent(engine.CameraComponent((2*10)+cameraWidth,(2*10)+cameraHeight,cameraWidth, cameraHeight))
            p4.getComponent('camera')._updateWorldPos(p4.getComponent('position').initialRect.x, p4.getComponent('position').initialRect.y)
            p4.getComponent('camera').trackEntity(p4)

def resetPlayer(entity):
    entity.getComponent('score').score = 0
    entity.getComponent('battle').lives = 3
    entity.getComponent('position').reset()
    entity.speed = 0
    entity.acceleration = entity.initialAcceleration
    entity.getComponent('camera')._updateWorldPos(entity.getComponent('position').initialRect.x, entity.getComponent('position').initialRect.y)
    entity.direction = 'right'
    entity.getComponent('imagegroups').alpha = 255
    entity.removeComponent('effect')
    entity.state = 'idle'
    if entity.hasComponent('camera'):
        entity.getComponent('camera').zoomLevel = 1
    if entity.hasComponent('transform'):
        entity.getComponent('transform').reset()
    if entity.hasComponent('motion'):
        entity.getComponent('motion').reset()

def playerInput(entity):
    
    if not entity.hasComponent('input'):
        return

    inputComponent = entity.getComponent('input')
    intentionComponent = entity.getComponent('intention')

    # up = jump
    if engine.inputManager.isDown(inputComponent.up):
        intentionComponent.jump = True
    else:
        intentionComponent.jump = False
    # left = moveLeft
    if engine.inputManager.isDown(inputComponent.left):
        intentionComponent.moveLeft = True
    else:
        intentionComponent.moveLeft = False
    # right = moveRight    
    if engine.inputManager.isDown(inputComponent.right):
        intentionComponent.moveRight = True
    else:
        intentionComponent.moveRight = False
    # down = balloon
    if engine.inputManager.isPressed(inputComponent.down):
        intentionComponent.fire = True
    else:
        intentionComponent.fire = False
    # b1 = zoom out
    if engine.inputManager.isDown(inputComponent.b1):
        intentionComponent.zoomOut = True
    else:
        intentionComponent.zoomOut = False        
    # b2 = zoom in
    if engine.inputManager.isDown(inputComponent.b2):
        intentionComponent.zoomIn = True
    else:
        intentionComponent.zoomIn = False

def makePlayer(x,y):
    entity = engine.Entity()
    entityIdleAnimation = engine.ImageGroup(idle0, idle1, idle2, idle3)
    entityWalkingAnimation = engine.ImageGroup(walking0, walking1, walking2, walking3, walking4, walking5, delay=6)
    entityJumpingAnimation = engine.ImageGroup(jumping)
    entity.acceleration = 0.3
    entity.initialAcceleration = entity.acceleration
    entity.reset = resetPlayer
    entity.addComponent(engine.Position(x,y,45,51))
    entity.getComponent('imagegroups').add('idle', entityIdleAnimation)
    entity.getComponent('imagegroups').add('walking', entityWalkingAnimation)
    entity.getComponent('imagegroups').add('jumping', entityJumpingAnimation)
    entity.addComponent(gamecomponents.Score())
    entity.addComponent(gamecomponents.Battle())
    entity.addComponent(engine.Intention())
    entity.addComponent(engine.Collider(10,1,25,50))
    entity.getComponent('tags').add('player')
    entity.addComponent(engine.Motion(acceleration=pygame.math.Vector2(0,0.3)))

    return entity

def makeCollision(x,y):
    entity = engine.Entity()
    entity.addComponent(engine.Position(x,y,1,1))
    entity.addComponent(engine.ParticleEmitter())
    entity.removeComponent('imagegroups')

    return entity

def makeExplosion(x,y):
    entity = engine.Entity()
    entity.addComponent(engine.Position(x,y,1,1))
    entity.addComponent(engine.ParticleEmitter(size=40, colour=engine.colours.BLUE))
    entity.removeComponent('imagegroups')

    return entity

balloon = pygame.image.load('images/balloon.png')

def makeBalloon(x,y):
    entity = engine.Entity()
    entityIdleImage = engine.ImageGroup(balloon)
    entity.acceleration = 0.3
    entity.initialAcceleration = entity.acceleration
    entity.addComponent(engine.Position(x,y,16,16))
    entity.getComponent('imagegroups').add('idle', entityIdleImage)
    entity.addComponent(engine.Collider(2,2,12,12))
    entity.getComponent('tags').add('balloon')
    entity.addComponent(engine.Motion(acceleration=pygame.math.Vector2(0,0.3)))

    return entity