import pygame
import engine

coin0 = pygame.image.load('images/coin_0.png')
coin1 = pygame.image.load('images/coin_1.png')
coin2 = pygame.image.load('images/coin_2.png')
coin3 = pygame.image.load('images/coin_3.png')
coin4 = pygame.image.load('images/coin_4.png')
coin5 = pygame.image.load('images/coin_5.png')

def makeCoin(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,23,23)
    entityAnimation = engine.Animation([coin1, coin2, coin3, coin4, coin5])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity
