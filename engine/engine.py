import pygame
import utils
import globals
import random
from .colours import *
from .entity_component_system import *

from .soundmanager import *
from .inputmanager import *
from .scenemanager import *

from .components import *
from .systems import *

sceneManager = SceneManager()
inputManager = InputManager()
soundManager = SoundManager()

clock = pygame.time.Clock()

def init(size, caption):
    global screen
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(caption)

def run():
    running = True
    while running:
    # game loop

        # check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        inputManager.processInput()
        soundManager.update()

        if sceneManager.isEmpty():
            running = False
        sceneManager.input(inputManager)
        sceneManager.update(inputManager)
        sceneManager.draw(screen) 

        clock.tick(60)

    # quit
    pygame.quit()

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

    def updateEntity(self, screen, inputStream, entity):

        # player collection of powerups
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'player' and entity.type != 'player':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # give the effect component to the player
                    otherEntity.effect = entity.effect
                    soundManager.playSound(entity.effect.sound)
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

class CollectionSystem(System):
    def check(self, entity):
        return entity.type == 'player' and entity.score is not None   
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'collectable':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # entity.collectable.onCollide(entity, otherEntity)
                    soundManager.playSound('coin')
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

class Score:
    def __init__(self):
        self.score = 0

class Battle:
    def __init__(self):
        self.lives = 3

class Effect:
    def __init__(self, apply, timer, sound, end):
        self.apply = apply
        self.timer = timer
        self.sound = sound
        self.end = end




