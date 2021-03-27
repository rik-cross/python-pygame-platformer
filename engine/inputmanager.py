import pygame

class PlayerInput:
    def __init__(self, controllerNumber, inputNumber, type, threshhold):
        self.controllerNumber = controllerNumber
        self.inputNumber = inputNumber
        self.type = type
        self.threshhold = threshhold

class Controller:
    def __init__(self, number):
        self.number = number
        self.joystick = None
        if number <= pygame.joystick.get_count()-1:
            self.joystick = pygame.joystick.Joystick(number)
            self.joystick.init()
            self.name = self.joystick.get_name()
        self.previousButtons = None
        self.currentButtons = None
        self.previousAxes = None
        self.currentAxes = None
        self.previousHats = None
        self.currentHats = None
    def processInput(self):
        if self.joystick is None:
            return
        self.previousButtons = self.currentButtons
        self.currentButtons = []
        for b in range(self.joystick.get_numbuttons()):
            self.currentButtons.append(self.joystick.get_button(b))
        self.previousAxes = self.currentAxes
        self.currentAxes = []
        for a in range(self.joystick.get_numaxes()):
            self.currentAxes.append(self.joystick.get_axis(a))
        self.previousHats = self.currentHats
        self.currentHats = []
        for h in range(self.joystick.get_numhats()):
            self.currentHats.append(self.joystick.get_hat(h))
    def isButtonDown(self, controllerInput):
        if self.currentButtons is None:
            return False
        if len(self.currentButtons) <= controllerInput.inputNumber:
            return False
        return self.currentButtons[controllerInput.inputNumber] >= controllerInput.threshhold
    def isButtonPressed(self, controllerInput):
        if self.currentButtons is None or self.previousButtons is None:
            return False
        if len(self.currentButtons) <= controllerInput.inputNumber:
            return False
        return self.currentButtons[controllerInput.inputNumber] >= controllerInput.threshhold and self.previousButtons[controllerInput.inputNumber] < controllerInput.threshhold
    def isButtonReleased(self, controllerInput):
        if len(self.currentButtons) <= controllerInput.inputNumber:
            return False
        if self.currentButtons is None or self.previousButtons is None:
            return False
        return self.currentButtons[controllerInput.inputNumber] <= controllerInput.threshhold and self.previousButtons[controllerInput.inputNumber] > controllerInput.threshhold
    
    def isHatDown(self, controllerInput):
        if self.currentHats is None:
            return False
        if len(self.currentHats) <= controllerInput.inputNumber[0]:
            return False
        if controllerInput.threshhold > 0:
            return self.currentHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] >= controllerInput.threshhold
        else:
            return self.currentHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] <= controllerInput.threshhold
    def isHatPressed(self, controllerInput):
        if self.currentHats is None or self.previousHats is None:
            return False
        if len(self.currentHats) <= controllerInput.inputNumber[0]:
            return False
        if controllerInput.threshhold > 0:
            return self.currentHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] >= controllerInput.threshhold and self.previousHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] < controllerInput.threshhold
        else:
            return self.currentHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] <= controllerInput.threshhold and self.previousHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] > controllerInput.threshhold
    def isHatReleased(self, controllerInput):
        if self.currentHats is None or self.previousHats is None:
            return False
        if len(self.currentHats) <= controllerInput.inputNumber[0]:
            return False
        if controllerInput.threshhold > 0:
            return self.currentHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] < controllerInput.threshhold and self.previousHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] >= controllerInput.threshhold
        else:
            return self.currentHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] > controllerInput.threshhold and self.previousHats[controllerInput.inputNumber[0]][controllerInput.inputNumber[1]] <= controllerInput.threshhold

    def isAxisDown(self, controllerInput):
        if self.currentAxes is None:
            return False
        if len(self.currentAxes) <= controllerInput.inputNumber:
            return False
        if controllerInput.threshhold > 0:
            return self.currentAxes[controllerInput.inputNumber] >= controllerInput.threshhold
        else:
            return self.currentAxes[controllerInput.inputNumber] <= controllerInput.threshhold
    def isAxisPressed(self, controllerInput):
        if self.currentAxes is None or self.previousAxes is None:
            return False
        if len(self.currentAxes) <= controllerInput.inputNumber:
            return False
        if controllerInput.threshhold > 0:
            return self.currentAxes[controllerInput.inputNumber] >= controllerInput.threshhold and self.previousAxes[controllerInput.inputNumber] < controllerInput.threshhold
        else:
            return self.currentAxes[controllerInput.inputNumber] <= controllerInput.threshhold and self.previousAxes[controllerInput.inputNumber] > controllerInput.threshhold
    def isAxisReleased(self, controllerInput):
        if self.currentAxes is None or self.previousAxes is None:
            return False
        if len(self.currentAxes) <= controllerInput.inputNumber:
            return False
        if controllerInput.threshhold > 0:
            return self.currentAxes[controllerInput.inputNumber] < controllerInput.threshhold and self.previousAxes[controllerInput.inputNumber] >= controllerInput.threshhold
        else:
            return self.currentAxes[controllerInput.inputNumber] > controllerInput.threshhold and self.previousAxes[controllerInput.inputNumber] <= controllerInput.threshhold

class Keyboard:
    def __init__(self):
        self.currentKeyStates = None
        self.previousKeyStates = None
    def processInput(self):
        self.previousKeyStates = self.currentKeyStates
        self.currentKeyStates = pygame.key.get_pressed()
    def isKeyDown(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == True
    def isKeyPressed(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == True and self.previousKeyStates[keyCode] == False
    def isKeyReleased(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == False and self.previousKeyStates[keyCode] == True

class InputManager:
    def __init__(self):
        self.keyboard = Keyboard()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        self.controllers = [Controller(n) for n in range(4)]
    def processInput(self):
        self.keyboard.processInput()
        for controller in self.controllers:
            controller.processInput()
    # TODO have as lists.
    def isDown(self, playerinput):
        if playerinput is None:
            return False
        if playerinput.type == 'button':
            return self.controllers[playerinput.controllerNumber].isButtonDown(playerinput)
        if playerinput.type == 'hat':
            return self.controllers[playerinput.controllerNumber].isHatDown(playerinput)
        if playerinput.type == 'axis':
            return self.controllers[playerinput.controllerNumber].isAxisDown(playerinput)
        if playerinput.type == 'key':
            return self.keyboard.isKeyDown(playerinput.inputNumber)             
    def isPressed(self, playerinput):
        if playerinput is None:
            return False
        if playerinput.type == 'button':
            return self.controllers[playerinput.controllerNumber].isButtonPressed(playerinput)
        if playerinput.type == 'hat':
            return self.controllers[playerinput.controllerNumber].isHatPressed(playerinput)
        if playerinput.type == 'axis':
            return self.controllers[playerinput.controllerNumber].isAxisPressed(playerinput)          
        if playerinput.type == 'key':
            return self.keyboard.isKeyPressed(playerinput.inputNumber)
    def isReleased(self, playerinput):
        if playerinput is None:
            return False
        if playerinput.type == 'button':
            return self.controllers[playerinput.controllerNumber].isButtonReleased(playerinput)
        if playerinput.type == 'hat':
            return self.controllers[playerinput.controllerNumber].isHatReleased(playerinput)
        if playerinput.type == 'axis':
            return self.controllers[playerinput.controllerNumber].isAxisReleased(playerinput)
        if playerinput.type == 'key':
            return self.keyboard.isKeyReleased(playerinput.inputNumber)
        
# inputs

class KeyInput:
    def __init__(self):

        self.enter = PlayerInput(0,pygame.K_RETURN,'key',1)
        self.esc = PlayerInput(0,pygame.K_ESCAPE,'key',1)

        self.w = PlayerInput(0,pygame.K_w,'key',1)
        self.a = PlayerInput(0,pygame.K_a,'key',1)
        self.s = PlayerInput(0,pygame.K_s,'key',1)
        self.d = PlayerInput(0,pygame.K_d,'key',1)
        self.q = PlayerInput(0,pygame.K_q,'key',1)
        self.e = PlayerInput(0,pygame.K_e,'key',1)

        self.i = PlayerInput(0,pygame.K_i,'key',1)
        self.k = PlayerInput(0,pygame.K_k,'key',1)
        self.j = PlayerInput(0,pygame.K_j,'key',1)
        self.l = PlayerInput(0,pygame.K_l,'key',1)
        self.u = PlayerInput(0,pygame.K_u,'key',1)
        self.o = PlayerInput(0,pygame.K_o,'key',1)

        self.n1 = PlayerInput(0,pygame.K_1,'key',1)

keys = KeyInput()

class ControllerInput:
    def __init__(self, number):

        self.a = PlayerInput(number,0,'button',1)
        self.b = PlayerInput(number,1,'button',1)
        self.x = PlayerInput(number,2,'button',1)
        self.y = PlayerInput(number,3,'button',1)

        self.leftShoulder = PlayerInput(number,4,'button',1)
        self.rightShoulder = PlayerInput(number,5,'button',1)

        self.select = PlayerInput(number,6,'button',1)
        self.start = PlayerInput(number,7,'button',1)

        self.leftTrigger = PlayerInput(number,2,'axis',0.1)
        self.rightTrigger = PlayerInput(number,5,'axis',0.1)

        self.dpad_left = PlayerInput(number, (0,0), 'hat', -1)
        self.dpad_right = PlayerInput(number, (0,0), 'hat', 1)
        self.dpad_up = PlayerInput(number, (0,1), 'hat', 1)
        self.dpad_down = PlayerInput(number, (0,1), 'hat', -1)

        self.leftDir_left = PlayerInput(number,0,'axis',-0.2)
        self.leftDir_right = PlayerInput(number,0,'axis',0.2)
        self.leftDir_up = PlayerInput(number,1,'axis',-0.2)
        self.leftDir_down = PlayerInput(number,1,'axis',0.2)

        self.rightDir_left = PlayerInput(number,3,'axis',-0.2)
        self.rightDir_right = PlayerInput(number,3,'axis',0.2)
        self.rightDir_up = PlayerInput(number,4,'axis',-0.2)
        self.rightDir_down = PlayerInput(number,4,'axis',0.2)

controller = [ ControllerInput(i) for i in range(4)]

