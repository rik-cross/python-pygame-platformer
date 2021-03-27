import pygame
import engine
import globals
import utils
import level
import scene


mainMenu = scene.MainMenuScene()
engine.sceneManager.push(mainMenu)

# create players
print('gamedata')
# player 1
globals.player1 = utils.makePlayer(300,50)
globals.player1.input = engine.Input(engine.keys.w, engine.keys.d, engine.keys.a, engine.keys.d, engine.keys.q, engine.keys.e)
# player 2
globals.player2 = utils.makePlayer(350,50)
globals.player2.input = engine.Input(engine.controller[0].dpad_up, engine.controller[0].dpad_down, engine.controller[0].dpad_left, engine.controller[0].dpad_right, engine.controller[0].a, engine.controller[0].b)
# player 3
globals.player3 = utils.makePlayer(400,50)
globals.player3.input = engine.Input(None, None, None, None, None, None)
# player 4
globals.player4 = utils.makePlayer(450,50)
globals.player4.input = engine.Input(None, None, None, None, None, None)

engine.soundManager.addMusic('solace', 'music/23 Solace.ogg')
engine.soundManager.addMusic('dawn', 'music/03 Before the Dawn.ogg')

engine.soundManager.addSound('jump', 'sounds/03_Jump_v2.ogg')
engine.soundManager.addSound('coin', 'sounds/01_Coin Pickup_v2.ogg')