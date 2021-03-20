import pygame
import engine
import utils
import level
import scene
import globals

mainMenu = scene.MainMenuScene()
engine.sceneManager.push(mainMenu)

# create players

# player 1
globals.player1 = utils.makePlayer(300,50)
globals.player1.input = engine.Input(engine.w, engine.s, engine.a, engine.d, engine.q, engine.e)
# player 2
globals.player2 = utils.makePlayer(350,50)
globals.player2.input = engine.Input(engine.i, engine.k, engine.j, engine.l, engine.u, engine.o)
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