import pygame
import engine
import globals
import utils
import level
import scene_main_menu
import game_tiles

# add scene
mainMenu = scene_main_menu.MainMenuScene()
engine.sceneManager.push(mainMenu)

engine.entityFactory.addEntity('player', utils.makePlayer)
engine.entityFactory.addEntity('coin', utils.makeCoin)
engine.entityFactory.addEntity('enemy', utils.makeEnemy)
engine.entityFactory.addEntity('collision', utils.makeCollision)
engine.entityFactory.addEntity('explosion', utils.makeExplosion)
engine.entityFactory.addEntity('balloon', utils.makeBalloon)
engine.entityFactory.addEntity('sign', utils.makeSign)

# create players

# player 1
globals.player1 = utils.makePlayer(300,50)
globals.player1.input = engine.Input(engine.keys.w, engine.keys.s, engine.keys.a, engine.keys.d, engine.keys.q, engine.keys.e)
globals.player1.input.inputFunc = utils.playerInput
globals.player1.imageGroups.hue = 90
globals.player1.tags.tags.append('player1')
# player 2
globals.player2 = utils.makePlayer(350,50)
globals.player2.input = engine.Input(engine.controller[0].dpad_up, engine.controller[0].dpad_down, engine.controller[0].dpad_left, engine.controller[0].dpad_right, engine.controller[0].a, engine.controller[0].b)
globals.player2.input.inputFunc = utils.playerInput
globals.player2.imageGroups.hue = 50
globals.player2.tags.tags.append('player2')
# player 3
globals.player3 = utils.makePlayer(400,50)
globals.player3.input = engine.Input(None, None, None, None, None, None)
globals.player3.input.inputFunc = utils.playerInput
globals.player3.imageGroups.hue = 300
globals.player3.tags.tags.append('player3')
# player 4
globals.player4 = utils.makePlayer(450,50)
globals.player4.input = engine.Input(None, None, None, None, None, None)
globals.player4.input.inputFunc = utils.playerInput
globals.player4.imageGroups.hue = 190
globals.player4.tags.tags.append('player4')

engine.soundManager.addMusic('solace', 'music/23 Solace.ogg')
engine.soundManager.addMusic('dawn', 'music/03 Before the Dawn.ogg')
engine.soundManager.addSound('jump', 'sounds/03_Jump_v2.ogg')
engine.soundManager.addSound('coin', 'sounds/01_Coin Pickup_v2.ogg')
engine.soundManager.addSound('blip', 'sounds/blip.wav')
engine.soundManager.addSound('explosion', 'sounds/explosion.wav')
engine.soundManager.addSound('explosion_small', 'sounds/explosion_small.wav')
engine.soundManager.addSound('powerup_appear', 'sounds/powerup_appear.wav')
engine.soundManager.addSound('powerup_get', 'sounds/powerup_get.wav')

engine.resourceManager.addImage('heart_small', 'images/heart_small.png')
engine.resourceManager.addFont('munro24', 'fonts/munro.ttf')