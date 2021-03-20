import pygame

class PlayerInput:
    def __init__(self, controllerNumber, inputNumber, type, threshhold):
        self.controllerNumber = controllerNumber
        self.inputNumber = inputNumber
        self.type = type
        self.threshhold = threshhold

class Controllers:
    def __init__(self):
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        self.controllers = [Controller(n) for n in range(4)]
    def processInput(self):
        for controller in self.controllers:
            controller.processInput()
    def isButtonDown(self, controllerInput):
        return self.controllers[controllerInput.controllerNumber].isButtonDown(controllerInput)
    def isButtonPressed(self, controllerInput):
        return self.controllers[controllerInput.controllerNumber].isButtonPressed(controllerInput)
    def isButtonReleased(self, controllerInput):
        return self.controllers[controllerInput.controllerNumber].isButtonReleased(controllerInput)

class Controller:
    def __init__(self, number):
        self.number = number
        self.joystick = None
        if number <= pygame.joystick.get_count()-1:
            self.joystick = pygame.joystick.Joystick(number)
            self.joystick.init()
        self.previousButtons = None
        self.currentButtons = None
    def processInput(self):
        if self.joystick is None:
            return
        self.previousButtons = self.currentButtons
        self.currentButtons = []
        for b in range(self.joystick.get_numbuttons()):
            self.currentButtons.append(self.joystick.get_button(b))
    def isButtonDown(self, controllerInput):
        if len(self.currentButtons) < controllerInput.inputNumber:
            return False
        return self.currentButtons[controllerInput.inputNumber] >= controllerInput.threshhold
    def isButtonPressed(self, controllerInput):
        if len(self.currentButtons) < controllerInput.inputNumber:
            return False
        if self.currentButtons is None or self.previousButtons is None:
            return False
        return self.currentButtons[controllerInput.inputNumber] >= controllerInput.threshhold and self.previousButtons[controllerInput.inputNumber] < controllerInput.threshhold
    def isButtonReleased(self, controllerInput):
        if len(self.currentButtons) < controllerInput.inputNumber:
            return False
        if self.currentButtons is None or self.previousButtons is None:
            return False
        return self.currentButtons[controllerInput.inputNumber] < controllerInput.threshhold and self.previousButtons[controllerInput.inputNumber] >= controllerInput.threshhold


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
        self.controllers = Controllers()
    def processInput(self):
        self.keyboard.processInput()
        self.controllers.processInput()
    def isDown(self, playerinput):
        if playerinput is None:
            return False
        if playerinput.type == 'button':
            return self.controllers.isButtonDown(playerinput)
        if playerinput.type == 'key':
            return self.keyboard.isKeyDown(playerinput.inputNumber)       
    def isPressed(self, playerinput):
        if playerinput is None:
            return False
        if playerinput.type == 'button':
            return self.controllers.isButtonPressed(playerinput)
        if playerinput.type == 'key':
            return self.keyboard.isKeyPressed(playerinput.inputNumber)
    def isReleased(self, playerinput):
        if playerinput is None:
            return False
        if playerinput.type == 'button':
            return self.controllers.isButtonReleased(playerinput)
        if playerinput.type == 'key':
            return self.keyboard.isKeyReleased(playerinput.inputNumber)
        
# inputs

enter = PlayerInput(0,pygame.K_RETURN,'key',1)
esc = PlayerInput(0,pygame.K_ESCAPE,'key',1)

w = PlayerInput(0,pygame.K_w,'key',1)
a = PlayerInput(0,pygame.K_a,'key',1)
s = PlayerInput(0,pygame.K_s,'key',1)
d = PlayerInput(0,pygame.K_d,'key',1)
q = PlayerInput(0,pygame.K_q,'key',1)
e = PlayerInput(0,pygame.K_e,'key',1)

i = PlayerInput(0,pygame.K_i,'key',1)
k = PlayerInput(0,pygame.K_k,'key',1)
j = PlayerInput(0,pygame.K_j,'key',1)
l = PlayerInput(0,pygame.K_l,'key',1)
u = PlayerInput(0,pygame.K_u,'key',1)
o = PlayerInput(0,pygame.K_o,'key',1)

n1 = PlayerInput(0,pygame.K_1,'key',1)

a0 = PlayerInput(0,0,'button',1)
b0 = PlayerInput(0,1,'button',1)
x0 = PlayerInput(0,2,'button',1)
y0 = PlayerInput(0,3,'button',1)