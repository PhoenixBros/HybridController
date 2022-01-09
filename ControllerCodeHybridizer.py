# written by PhoenixBros
# written in python 3.10.1 sorry if it breaks for you
# becuase this system creates a virtual controller and uses your existing controller as input you may have to restart games or change which controller they use in settings 
# i tested this code using a ps4 controller. your controller may provide different numbers for its inputs. add a controlScheme to reprisent your controller and switch to it

# TODO this code does not support hats
# TODO this code does not support converting axis input to button and button to axis

import pygame
import vgamepad as vg
import random

############## control schemes ##############
# the scheme maps the controllers values to the corrisponding xbox input
# a number must exist for each input found in inputOptions. dont double up becuase the key and values will be reversed
# this can also be used to create "wrong" schemes that can do fun stuff like flip your x and y axis or remap the controller
# example of a scheme for a ps4 controller (objectivly best controller acording to me)
PS4SCHEME = {'button':{'a':0, 'b':1, 'x':2, 'y':3, 'back':4, 'guide':5, 'start':6, 'left thumb':7, 'right thumb':8, 'left shoulder':9, 'right shoulder':10, 'dpad up':11, 'dpad down':12, 'dpad left':13, 'dpad right':14, 'track pad':15}, 'axis':{'left stick x':0, 'left stick y':1, 'right stick x':2, 'right stick y':3, 'left trigger':4, 'right trigger':5}}
# example of a warped scheme that makes: a->y, b->x, x->b, y->a and lstick x->lstick y, rstick x->rstick y
PS4FLIPED = {'button':{'a':3, 'b':2, 'x':1, 'y':0, 'back':4, 'guide':5, 'start':6, 'left thumb':7, 'right thumb':8, 'left shoulder':9, 'right shoulder':10, 'dpad up':12, 'dpad down':11, 'dpad left':14, 'dpad right':13, 'track pad':15}, 'axis':{'left stick x':1, 'left stick y':0, 'right stick x':3, 'right stick y':2, 'left trigger':4, 'right trigger':5}}

class HybridController:
    # XBOX BUTTONS
    XBOX_DPAD_UP = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
    XBOX_DPAD_DOWN = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
    XBOX_DPAD_LEFT = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
    XBOX_DPAD_RIGHT = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
    XBOX_START = vg.XUSB_BUTTON.XUSB_GAMEPAD_START
    XBOX_BACK = vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
    XBOX_LEFT_THUMB = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
    XBOX_RIGHT_THUMB = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
    XBOX_LEFT_SHOULDER = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    XBOX_RIGHT_SHOULDER = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
    XBOX_GUIDE = vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
    XBOX_A = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
    XBOX_B = vg.XUSB_BUTTON.XUSB_GAMEPAD_B
    XBOX_X = vg.XUSB_BUTTON.XUSB_GAMEPAD_X
    XBOX_Y = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y

    ############################################
    ############### global variables ###########
    # the current condition of the controller and code
    pg = pygame
    con = {"button":{'a':False, 'b':False, 'x':False, 'y':False, 'back':False, 'guide':False, 'start':False, 'left thumb':False, 'right thumb':False, 'left shoulder':False, 'right shoulder':False, 'dpad up':False, 'dpad down':False, 'dpad left':False, 'dpad right':False}, "axis":{'left stick x':0, 'left stick y':0, 'right stick x':0, 'right stick y':0, 'left trigger':0, 'right trigger':0}}
    code = {"button":{'a':False, 'b':False, 'x':False, 'y':False, 'back':False, 'guide':False, 'start':False, 'left thumb':False, 'right thumb':False, 'left shoulder':False, 'right shoulder':False, 'dpad up':False, 'dpad down':False, 'dpad left':False, 'dpad right':False}, "axis":{'left stick x':0, 'left stick y':0, 'right stick x':0, 'right stick y':0, 'left trigger':0, 'right trigger':0}}
    inputOptions = ['a', 'b', 'x', 'y', 'back', 'guide', 'start', 'left thumb', 'right thumb', 'left shoulder', 'right shoulder', 'dpad up', 'dpad down', 'dpad left', 'dpad right', 'left stick x', 'left stick y', 'right stick x', 'right stick y', 'left trigger','right trigger']
    activeScheme = {}
    revScheme = {}
    buttonSet = []
    axisSet = []
    activeMode = []
    joyce = pg.joystick.Joystick
    virtcon = vg.VX360Gamepad

    # initilize the controller settup
    def __init__(self, scheme:dict[str, any]):
        self.pg.init()
        # only continues if a controller is conected
        if (self.pg.joystick.get_count() < 1): 
            print("no controller connected.")
        else:
            self.joyce = self.connectController()
            self.virtcon = self.createVirtualController()
            self.activeScheme = scheme
            self.revScheme = self.reverseScheme(self.activeScheme)
            self.readController(self.joyce, self.activeScheme) 
            self.activeMode = ['joy','joy']

    #############################################
    ################# functions #################
    # reads the currenct condition of the controller and saves it to variables
    def readController(self, joy: pygame.joystick.Joystick, scheme: dict[str, dict[str, int]]):
        button = scheme['button']
        axis = scheme['axis']
        self.con = {"button":{
                        'a':bool(joy.get_button(button['a'])), 
                        'b':bool(joy.get_button(button['b'])), 
                        'x':bool(joy.get_button(button['x'])), 
                        'y':bool(joy.get_button(button['y'])), 
                        'back':bool(joy.get_button(button['back'])), 
                        'guide':bool(joy.get_button(button['guide'])), 
                        'start':bool(joy.get_button(button['start'])), 
                        'left thumb':bool(joy.get_button(button['left thumb'])), 
                        'right thumb':bool(joy.get_button(button['right thumb'])), 
                        'left shoulder':bool(joy.get_button(button['left shoulder'])), 
                        'right shoulder':bool(joy.get_button(button['right shoulder'])), 
                        'dpad up':bool(joy.get_button(button['dpad up'])), 
                        'dpad down':bool(joy.get_button(button['dpad down'])), 
                        'dpad left':bool(joy.get_button(button['dpad left'])), 
                        'dpad right':bool(joy.get_button(button['dpad right']))},
                    "axis":{
                        'left stick x':self.clampf(joy.get_axis(axis['left stick x'])),
                        'left stick y':self.clampf(-joy.get_axis(axis['left stick y'])), 
                        'right stick x':self.clampf(joy.get_axis(axis['right stick x'])),
                        'right stick y':self.clampf(-joy.get_axis(axis['right stick x'])), 
                        'left trigger':self.triggerSquash(joy.get_axis(axis['left trigger'])), 
                        'right trigger':self.triggerSquash(joy.get_axis(axis['right trigger']))}}

    # individually reads a button
    def readButton(self, button: str, joy: pygame.joystick.Joystick, scheme: dict[str, int]):
        self.con["button"][button] = bool(joy.get_button(scheme[button]))

    # individually reads an axis
    def readAxis(self, axis: str, joy: pygame.joystick.Joystick, scheme: dict[str, int]):
        if axis in self.inputOptions[15:]:
            if len(axis.split(' ')) == 3:
                if axis.split(' ')[2] == 'x':
                    self.con["axis"][axis] = self.clampf(joy.get_axis(scheme[axis]))
                else:
                    self.con["axis"][axis] = self.clampf(-joy.get_axis(scheme[axis]))
            else:
                self.con["axis"][axis] = self.triggerSquash(joy.get_axis(scheme[axis]))

    # codes set button function
    def setButton(self, button:str, val:bool):
        self.code["button"][button] = val
        self.buttonSet.append(self.indexFromButtonStr(button))
    def setButton(self, key:int, val:bool):
        self.code["button"][self.strFromButtonIndex(key)] = val
        self.buttonSet.append(key)

    # codes set axis function
    def setAxis(self, name:str, val:float):
        self.code["axis"][name] = self.clampf(val) 
        self.axisSet.append(self.indexFromAxisStr(name))
    def setAxis(self, ind:int, val:float):
        self.code["axis"][self.strFromAxisIndex(ind)] = self.clampf(val)
        self.axisSet.append(ind)

    # sets the output controllers values
    def updateController(self, gamepad: vg.VX360Gamepad, bMode: str, aMode: str, scheme: dict[str, dict[str, int]]):
        for i in range(15):
            butt = scheme["button"][self.strFromButtonIndex(i)]
            activation = self.combineButton(butt, bMode)
            if activation:
                gamepad.press_button(self.hexButtonIndex(butt))
            else:
                gamepad.release_button(self.hexButtonIndex(butt))
        gamepad.left_joystick_float(self.combineAxis(scheme["axis"]['left stick x'], aMode), self.combineAxis(scheme["axis"]['left stick y'], aMode))
        gamepad.right_joystick_float(self.combineAxis(scheme["axis"]['right stick x'], aMode), self.combineAxis(scheme["axis"]['right stick y'], aMode))
        gamepad.left_trigger_float(self.combineAxis(scheme["axis"]['left trigger'], aMode))
        gamepad.right_trigger_float(self.combineAxis(scheme["axis"]['right trigger'], aMode))
        gamepad.update()

    # updates individual buttons
    def updateButton(self, key: int, gamepad: vg.VX360Gamepad, bMode: str, scheme:dict[str, int] ):
        key = scheme[self.strFromButtonIndex(key)]
        activation = self.combineButton(key, bMode)
        if activation:
            gamepad.press_button(self.hexButtonIndex(key))
        else:
            gamepad.release_button(self.hexButtonIndex(key))
        gamepad.update()
        return key

    # updates individule axis
    def updateAxis(self, key: int, gamepad: vg.VX360Gamepad, aMode: str, scheme: dict[str, int]):
        if key < 2:
            gamepad.left_joystick_float(self.combineAxis(scheme['left stick x'], aMode), self.combineAxis(scheme['left stick y'], aMode))
        elif key < 4:
            gamepad.right_joystick_float(self.combineAxis(scheme['right stick x'], aMode), self.combineAxis(scheme['right stick y'], aMode))
        elif key < 5:
            gamepad.left_trigger_float(self.combineAxis(scheme['left trigger'], aMode))
        elif key < 6:
            gamepad.right_trigger_float(self.combineAxis(scheme['right trigger'], aMode))
        gamepad.update()
        return key

    # randomizes the values of the code side
    def randomize(self):
        for i in range(15):
            if i != 4 and i != 5 and i != 6:
                self.code['button'][self.strFromButtonIndex(i)] = random.randint(0,1) == 1
        self.code['axis']['left stick x'] = random.random()*2-1
        self.code['axis']['left stick y'] = random.random()*2-1
        self.code['axis']['right stick x'] = random.random()*2-1
        self.code['axis']['right stick y'] = random.random()*2-1
        self.code['axis']['left trigger'] = random.randint(0,1)*random.random()
        self.code['axis']['right trigger'] = random.randint(0,1)*random.random()

    # connects to the active controller
    def connectController(self):
        joy = self.pg.joystick.Joystick(0)
        joy.init()
        print("controller conected!", joy.get_name())
        return joy

    # creates and activates the virtual xbox controller that we can screw with
    def createVirtualController(self):
        gamepad = vg.VX360Gamepad() 
        # presses the a button then releases to inform windows of the controller
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update
        return gamepad

    # The main update function
    def updatefull(self, joy:pygame.joystick.Joystick, gamepad:vg.VX360Gamepad, scheme:dict[str, dict[str, int]], modes:list[str]):
        for event in self.pg.event.get((pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYDEVICEREMOVED)):
            if (event.type == pygame.JOYBUTTONDOWN) | (event.type == pygame.JOYBUTTONUP):
                if event.button < 15:
                    button = event.button
                    self.readButton(self.revScheme["button"][button], joy, scheme["button"])
                    self.updateButton(button, gamepad, modes[0], scheme["button"])
            elif event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                self.readAxis(self.revScheme["axis"][axis], joy, scheme["axis"])
                self.updateAxis(axis, gamepad, modes[1], scheme["axis"])
            elif event.type == self.pg.JOYDEVICEREMOVED :
                print("controller disconnected")
        while len(self.buttonSet) > 0:
            button = self.buttonSet.pop()
            if button < 15:
                self.updateButton(button, gamepad, modes[0], scheme["button"])
        while len(self.axisSet) > 0:
            axis = self.axisSet.pop()
            if axis < 6:
                self.updateAxis(axis, gamepad, modes[1], scheme["axis"])
    def updatepart(self, scheme:dict[str, dict[str, int]], modes:list[str]):
        self.updatefull(self.joyce, self.virtcon, scheme, modes)
    def update(self):
        self.updatefull(joy=self.joyce, gamepad=self.virtcon, scheme=self.activeScheme, modes=self.activeMode)

    # print the current controller values
    def printController(self, control:dict[str, any]):
        for i in control:
            for j in control[i]:
                print(i + ":" + str(j) + " = " + str(control[i][j]))

    # changes the active scheme, usful for activly remaping the controller
    def setscheme(self, newscheme:dict[str, dict[str, bool]]):
        self.activeScheme = newscheme

    # changes the active mode
    def setModes(self, newmode:list[str]):
        self.activeMode = newmode

    # sets the joystick
    def setJoystick(self, newJoy:pygame.joystick.Joystick):
        self.joyce = newJoy

    # sets the virtual controller
    def setVirtualControler(self, newVirt:vg.VX360Gamepad):
        self.virtcon = newVirt

    ################### helpers ######################
    # locks value to between -1 and 1
    def clampf(self, n: float):
        return max(min(1, n), -1)

    # squashes the -1 to 1 into 0 to 1
    def triggerSquash(self, n:float):
        return self.clampf((n+1)/2)

    # returns the button hex code by index
    def hexButtonIndex(self, ind:int):
        buttons = [self.XBOX_A, self.XBOX_B, self.XBOX_X, self.XBOX_Y, self.XBOX_BACK, self.XBOX_GUIDE, self.XBOX_START, self.XBOX_LEFT_THUMB, self.XBOX_RIGHT_THUMB, self.XBOX_LEFT_SHOULDER, self.XBOX_RIGHT_SHOULDER, self.XBOX_DPAD_UP, self.XBOX_DPAD_DOWN, self.XBOX_DPAD_LEFT, self.XBOX_DPAD_RIGHT]
        if ind in range(15):
            return buttons[ind]
        else:
            return 0x0

    # returns the button string name by index
    def strFromButtonIndex(self, ind: int):
        if ind in range(15):
            return self.inputOptions[ind]
        else:
            return 'null'
    def indexFromButtonStr(self, st: str):
        return self.inputOptions.index(st)

    # returns axis name by index
    def strFromAxisIndex(self, ind: int):
        axis = ['left stick x', 'left stick y', 'right stick x', 'right stick y', 'left trigger', 'right trigger']
        if ind in range(6):
            return axis[ind]
        else:
            return 'null'
    def indexFromAxisStr(self, st:str):
        axis = ['left stick x', 'left stick y', 'right stick x', 'right stick y', 'left trigger', 'right trigger']
        return axis.index(st)
    
    # reverses the value and keys in scheme
    def reverseScheme(self, scheme):
        rev = {}
        for j in scheme:
            rev[j] = {}
            for i in scheme[j]:
                rev[j][scheme[j][i]] = i
        return rev

    # sets the controllers saved status to defualt
    def resetCon(self):
        self.con = {"button":{'a':False, 'b':False, 'x':False, 'y':False, 'back':False, 'guide':False, 'start':False, 'left thumb':False, 'right thumb':False, 'left shoulder':False, 'right shoulder':False, 'dpad up':False, 'dpad down':False, 'dpad left':False, 'dpad right':False}, "axis":{'left stick x':0, 'left stick y':0, 'right stick x':0, 'right stick y':0, 'left trigger':0, 'right trigger':0}}

    # sets the codes saved status to defualt
    def resetCode(self):
        self.code = {"button":{'a':False, 'b':False, 'x':False, 'y':False, 'back':False, 'guide':False, 'start':False, 'left thumb':False, 'right thumb':False, 'left shoulder':False, 'right shoulder':False, 'dpad up':False, 'dpad down':False, 'dpad left':False, 'dpad right':False}, "axis":{'left stick x':0, 'left stick y':0, 'right stick x':0, 'right stick y':0, 'left trigger':0, 'right trigger':0}}

    ###################################################
    ################# combination methods #############
    # adding more modes of combination can do some fun stuff
    # returns a value based on both inputs and the combination method
    def combineButton(self, key: int, mode: str) -> bool:
        cod = self.code['button'][self.strFromButtonIndex(key)]
        joy = self.con['button'][self.strFromButtonIndex(key)]
        if mode == 'or':
            return cod | joy
        elif mode == 'xor':
            return (~cod & joy) | (cod & ~joy)
        elif mode == 'and':
            return cod & joy
        elif mode == 'rand':
            r = random.randint(0,1) == 1
            return (cod & r) | (joy & ~r)
        elif mode == 'joy':
            return joy
        elif mode == 'code':
            return cod

    # returns a float based on both inputs and the combination method
    def combineAxis(self, key: int, mode: str) -> float:
        cod = self.code['axis'][self.strFromAxisIndex(key)]
        joy = self.con['axis'][self.strFromAxisIndex(key)]
        if mode == 'max':
            if abs(cod) > abs(joy):
                return cod
            else: 
                return joy
        elif mode == 'min':
            if abs(cod) > abs(joy):
                return joy
            else: 
                return cod
        elif mode == 'joy':
            return joy
        elif mode == 'code':
            return cod
        elif mode == "avg":
            return (cod + joy) / 2

##################################################
##################### main #######################
if __name__ == '__main__':
    cntr = HybridController(PS4SCHEME) 
    cntr.setModes(["xor","max"])
    # this is a simple loop, and can be replaced by calling update() if this code is called from another file
    coderunning = True
    while coderunning:
        # sets a framerate
        cntr.pg.time.Clock().tick(60)
        # updates the system
        cntr.update()
        cntr.updatefull(joy=cntr.joyce, gamepad=cntr.virtcon, scheme=PS4SCHEME, modes=["xor","max"]) 
        