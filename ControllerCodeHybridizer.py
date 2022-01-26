# written by PhoenixBros
# written in python 3.10.1 
# becuase this system creates a virtual controller and uses your existing controller as input you may have to restart games or change which controller they use in settings 
# i tested this code using a ps4 controller and a moga. your controller may provide different numbers for its inputs. add a controlScheme to reprisent your controller and switch to it

import pygame
import vgamepad as vg
import random

############## control schemes ##############
# the scheme records what the key is for each button, axis, or hat that your controller uses. make sure these are accurate to your controller
# the map determines what these buttons and axis influence. these do not need to map accurately and can be used to create unusual behavior.
# example of a scheme for a ps4 controller (objectivly best controller)
PS4SCHEME = {'button':{'x':0, 'circle':1, 'square':2, 'triangle':3, 'share':4, 'guide':5, 'options':6, 'left thumb':7, 'right thumb':8, 'left shoulder':9, 'right shoulder':10, 'dpad up':11, 'dpad down':12, 'dpad left':13, 'dpad right':14, 'track pad':15}, 
            "axis":{'left stick x':0, 'left stick y':1, 'right stick x':2, 'right stick y':3, 'left trigger':4, 'right trigger':5}}
PS4DEFAULTMAP = {   'x':[{'key':'a','type':'button'}], 
                    'circle':[{'key':'b','type':'button'}], 
                    'square':[{'key':'x','type':'button'}],
                    'triangle':[{'key':'y','type':'button'}],
                    'share':[{'key':'back','type':'button'}],
                    'guide':[{'key':'guide','type':'button'}],
                    'options':[{'key':'start','type':'button'}],
                    'left thumb':[{'key':'left thumb','type':'button'}],
                    'right thumb':[{'key':'right thumb','type':'button'}],
                    'left shoulder':[{'key':'left shoulder','type':'button'}],
                    'right shoulder':[{'key':'right shoulder','type':'button'}],
                    'dpad up':[{'key':'dpad up','type':'button'}],
                    'dpad down':[{'key':'dpad down','type':'button'}],
                    'dpad left':[{'key':'dpad left','type':'button'}],
                    'dpad right':[{'key':'dpad right','type':'button'}],
                    'track pad':[{'key':'start','type':'button'}],
                    'left stick x':[{'key':'left stick x','type':'axis', 'flip':False}],
                    'left stick y':[{'key':'left stick y','type':'axis', 'flip':True}],
                    'right stick x':[{'key':'right stick x','type':'axis', 'flip':False}],
                    'right stick y':[{'key':'right stick y','type':'axis', 'flip':True}],
                    'left trigger':[{'key':'left trigger','type':'axis', 'squash':True}],
                    'right trigger':[{'key':'right trigger','type':'axis', 'squash':True}]}
# example of the MOGA controler
MOGASCHEME = {"button":{'a':0, 'b':1, 'x':2, 'y':3, 'back':6, 'start':7, 'left thumb':8, 'right thumb':9, 'left shoulder':4, 'right shoulder':5},
             "axis":{'left stick x':0, 'left stick y':1, 'right stick x':2, 'right stick y':3, 'left trigger':4, 'right trigger':5}, 
             "hat":{'hat':0, 'hat x':0, 'hat y':1}}
MOGADEFAULTMAP = {  'a':[{'key':'a','type':'button'}], 
                    'b':[{'key':'b','type':'button'}], 
                    'x':[{'key':'x','type':'button'}],
                    'y':[{'key':'y','type':'button'}],
                    'back':[{'key':'back','type':'button'}],
                    'start':[{'key':'start','type':'button'}],
                    'left thumb':[{'key':'left thumb','type':'button'}],
                    'right thumb':[{'key':'right thumb','type':'button'}],
                    'left shoulder':[{'key':'left shoulder','type':'button'}],
                    'right shoulder':[{'key':'right shoulder','type':'button'}],
                    'hat y':[{'key':'dpad up','type':'button', 'val':1},
                            {'key':'dpad down','type':'button', 'val':-1}],
                    'hat x':[{'key':'dpad left','type':'button', 'val':-1},
                            {'key':'dpad right','type':'button', 'val':1}],
                    'left stick x':[{'key':'left stick x','type':'axis', 'flip':False}],
                    'left stick y':[{'key':'left stick y','type':'axis', 'flip':False}],
                    'right stick x':[{'key':'right stick x','type':'axis', 'flip':False}],
                    'right stick y':[{'key':'right stick y','type':'axis', 'flip':False}],
                    'left trigger':[{'key':'left trigger','type':'axis', 'flip':False}],
                    'right trigger':[{'key':'right trigger','type':'axis', 'flip':False}]}

# example of an unusual map
# [{'(input name)':{'key':'(output name), 'type':'(input type)', 'val':'(threshold or output)', 'flip':(true/false), 'squash':(true/false)}]
# (input name) is the name of the input used by your controller.
# (output name) is the name of the input on the xbox controller.
# (input type) is what kind of input this output is
# (threshold or output) is the threshold of converting a float to a bool. or its the float value that it will output
# (flip) allows for inversion of up and down
# (squash) is if the input should be forced 0 to 1 from -1 to 1
# only add 1 instance of each input. if you need multiple, simply add a another dict portion 
# this map swaps the dpad with the left joystick
PS4DEMOMAP = {  'x':[{'key':'a', 'type':'button'}], 
                'circle':[{'key':'b', 'type':'button'}], 
                'square':[{'key':'x', 'type':'button'}],
                'triangle':[{'key':'y', 'type':'button'}],
                'share':[{'key':'back', 'type':'button'}],
                'guide':[{'key':'guide', 'type':'button'}],
                'options':[{'key':'start', 'type':'button'}],
                'left thumb':[{'key':'left thumb', 'type':'button'}],
                'right thumb':[{'key':'right thumb', 'type':'button'}],
                'left shoulder':[{'key':'left shoulder', 'type':'button'}],
                'right shoulder':[{'key':'right shoulder', 'type':'button'}],
                'track pad':[{'key':'start','type':'button'}],
                'dpad up':[{'key':'left stick y', 'type':'axis', 'val':1.0}],
                'dpad down':[{'key':'left stick y', 'type':'axis', 'val':-1.0}],
                'dpad left':[{'key':'left stick x', 'type':'axis', 'val':-1.0}],
                'dpad right':[{'key':'left stick x', 'type':'axis', 'val':1.0}],
                'left stick x':[{'key':'dpad left', 'type':'button', 'val':-.5, 'flip':False},
                                {'key':'dpad right', 'type':'button', 'val':.5, 'flip':False}],
                'left stick y':[{'key':'dpad up', 'type':'button', 'val':-.5, 'flip':False},
                                {'key':'dpad down', 'type':'button', 'val':.5, 'flip':False}],
                'right stick x':[{'key':'right stick x', 'type':'axis', 'flip':False}],
                'right stick y':[{'key':'right stick y', 'type':'axis', 'flip':True}],
                'left trigger':[{'key':'left trigger', 'type':'axis', 'squash':True}],
                'right trigger':[{'key':'right trigger', 'type':'axis', 'squash':True}]}

class HybridController:
    ################ constants ###############
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
    
    INPUTOPTIONS = ['a', 'b', 'x', 'y', 'back', 'guide', 'start', 'left thumb', 'right thumb', 'left shoulder', 'right shoulder', 'dpad up', 'dpad down', 'dpad left', 'dpad right', 'left stick x', 'left stick y', 'right stick x', 'right stick y', 'left trigger', 'right trigger']

    ############################################
    ############### class variables ###########
    pg = pygame

    # the current condition of the controller and code
    con = {"button":{'a':False, 'b':False, 'x':False, 'y':False, 'back':False, 'guide':False, 'start':False, 'left thumb':False, 'right thumb':False, 'left shoulder':False, 'right shoulder':False, 'dpad up':False, 'dpad down':False, 'dpad left':False, 'dpad right':False}, "axis":{'left stick x':0, 'left stick y':0, 'right stick x ':0, 'right stick y':0, 'left trigger':0, 'right trigger':0}}
    code = {"button":{'a':False, 'b':False, 'x':False, 'y':False, 'back':False, 'guide':False, 'start':False, 'left thumb':False, 'right thumb':False, 'left shoulder':False, 'right shoulder':False, 'dpad up':False, 'dpad down':False, 'dpad left':False, 'dpad right':False}, "axis":{'left stick x':0, 'left stick y':0, 'right stick x':0, 'right stick y':0, 'left trigger':0, 'right trigger':0}}

    # defualt perameters
    activeMap = {}
    activeScheme = {}
    buttonSet = []
    axisSet = []
    activeMode = []
    joyce = pygame.joystick.Joystick
    virtcon = vg.VX360Gamepad

    # initilize the controller settup
    def __init__(self, scheme:dict[str, any], map:dict[str, any]):
        self.pg.init()
        # only continues if a controller is conected
        if (self.pg.joystick.get_count() < 1): 
            print("no controller connected.")
        else:
            self.joyce = self.connectController()
            self.virtcon = self.createVirtualController()
            self.activeScheme = scheme
            self.activeMap = map
            self.activeMode = ['joy','joy']
            self.readController(self.joyce, self.activeScheme, self.activeMap) 

    #############################################
    ################# functions #################
    # reads the currenct condition of the controller and saves it to variables
    def readController(self, joy: pygame.joystick.Joystick, scheme: dict[str, dict[str, int]], map: dict[str, any]):
        # reads the buttons
        if scheme.__contains__("button"):
            for key in scheme["button"].keys():
                for mkey in map[key]:
                    if mkey['type'] == 'button':
                        self.con["button"][mkey['key']] = joy.get_button(scheme["button"][key])
                    elif mkey["type"] == 'axis':
                        self.con["axis"][mkey['key']] = self.cnvrtBtnToAxs(joy.get_button(scheme["button"][key]), mkey)
        
        # reads the axis
        if scheme.__contains__("axis"):
            for key in scheme["axis"].keys():
                for mkey in map[key]:
                    # the joy value
                    val = joy.get_axis(scheme["axis"][key])
                    
                    # can invert the value
                    if mkey.__contains__('flip'):
                        if mkey['flip']:
                            val = -1.0*val
                    
                    # can squash the value from [-1,1] to [0,1]
                    if mkey.__contains__('squash'):
                        if mkey['squash']:
                            val = self.triggerSquash(val)

                    # turns it into an axis or button output
                    if mkey['type'] == 'axis': 
                        self.con["axis"][mkey['key']] = val
                    elif mkey['type'] == 'button':
                        self.con["button"][mkey['key']] = self.cnvrtAxsToBtn(val, mkey)
        
        # reads hats
        if scheme.__contains__("hat"):
            hat = scheme["hat"]
            for mkeyx in map['hat x']:
                if mkeyx['type'] == 'button':
                    self.con["button"][mkeyx['key']] = self.cnvrtHatToBtn(joy.get_hat(hat['hat'])[hat['hat x']], mkeyx)
                elif mkeyx['type'] == 'axis':
                    self.con["axis"][mkeyx['key']] = self.cnvrtHatToAxs(joy.get_hat(hat['hat'])[hat['hat x']], mkeyx)
 
            for mkeyy in map['hat y']:
                if mkeyy['type'] == 'button':
                    self.con["button"][mkeyy['key']] = self.cnvrtHatToBtn(joy.get_hat(hat['hat'])[hat['hat y']], mkeyy)
                elif mkeyy['type'] == 'axis':
                    self.con["axis"][mkeyy['key']] = self.cnvrtHatToAxs(joy.get_hat(hat['hat'])[hat['hat y']], mkeyy)
        self.updateController(self.virtcon, self.activeMode[0], self.activeMode[1])
    
    # individually reads a button
    def readButton(self, button: str, joy: pygame.joystick.Joystick, scheme: dict[str, int], map: dict[str, dict[any]]):
        if map.__contains__(button):
            for mkey in map[button]:
                if mkey['type'] == 'button':
                    self.con["button"][mkey['key']] = joy.get_button(scheme[button])
                elif mkey["type"] == 'axis':
                    self.con["axis"][mkey['key']] = self.cnvrtBtnToAxs(joy.get_button(scheme[button]), mkey)

    # individually reads an axis
    def readAxis(self, axis: str, joy: pygame.joystick.Joystick, scheme: dict[str, int], map: dict[str, dict[any]]):
        for mkey in map[axis]:
            # the joy value
            val = joy.get_axis(scheme[axis])
            
            # can invert the value
            if mkey.__contains__('flip'):
                if mkey['flip']:
                    val = -1.0*val
            
            # can squash the value from [-1,1] to [0,1]
            if mkey.__contains__('squash'):
                if mkey['squash']:
                    val = self.triggerSquash(val)

            # turns it into an axis or button output
            if mkey['type'] == 'axis':
                self.con["axis"][mkey['key']] = val
            elif mkey['type'] == 'button':
                self.con["button"][mkey['key']] = self.cnvrtAxsToBtn(val, mkey)

    # reads the value of a hat
    def readHat(self, hit: int, joy: pygame.joystick.Joystick, scheme: dict[str, int], map: dict[str, dict[any]]):
        hat = scheme["hat"]
        for mkeyx in map['hat x']:
            if mkeyx['type'] == 'button':
                self.con["button"][mkeyx['key']] = self.cnvrtHatToBtn(joy.get_hat(hit)[hat['hat x']], mkeyx)
            elif mkeyx['type'] == 'axis':
                self.con["axis"][mkeyx['key']] = self.cnvrtHatToAxs(joy.get_hat(hit)[hat['hat x']], mkeyx)
        
        for mkeyy in map['hat y']:
            if mkeyy['type'] == 'button':
                self.con["button"][mkeyy['key']] = self.cnvrtHatToBtn(joy.get_hat(hit)[hat['hat y']], mkeyy)
                self.updateButton(mkeyy['key'], self.virtcon, self.activeMode)
            elif mkeyy['type'] == 'axis':
                self.con["axis"][mkeyy['key']] = self.cnvrtHatToAxs(joy.get_hat(hit)[hat['hat y']], mkeyy)
                self.updateAxis(mkeyy['key'], self.virtcon, self.activeMode)
        
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
    def updateController(self, gamepad: vg.VX360Gamepad, bMode: str, aMode: str):
        for i in range(15):
            activation = self.combineButton(i, bMode)
            if activation:
                gamepad.press_button(self.hexButtonIndex(i))
            else:
                gamepad.release_button(self.hexButtonIndex(i))
        gamepad.left_joystick_float(self.combineAxis(0, aMode), self.combineAxis(1, aMode))
        gamepad.right_joystick_float(self.combineAxis(2, aMode), self.combineAxis(3, aMode))
        gamepad.left_trigger_float(self.combineAxis(4, aMode))
        gamepad.right_trigger_float(self.combineAxis(5, aMode))
        gamepad.update()

    # updates individual buttons
    def updateButton(self, key: str, gamepad: vg.VX360Gamepad, bMode: str):
        key = self.indexFromButtonStr(key)
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
            gamepad.left_joystick_float(self.combineAxis(0, aMode), self.combineAxis(1, aMode))
        elif key < 4:
            gamepad.right_joystick_float(self.combineAxis(2, aMode), self.combineAxis(3, aMode))
        elif key < 5:
            gamepad.left_trigger_float(self.combineAxis(4, aMode))
        elif key < 6:
            gamepad.right_trigger_float(self.combineAxis(5, aMode))
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
    def updatefull(self, joy:pygame.joystick.Joystick, gamepad:vg.VX360Gamepad, scheme:dict[str, dict[str, int]], map:dict[str, any], modes:list[str]):
        self.virtcon = gamepad
        self.activeMode = modes
        changed = False
        # cycle through the events and perform action if need be
        for event in self.pg.event.get((pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION, pygame.JOYDEVICEREMOVED)):
            if (event.type == pygame.JOYBUTTONDOWN) | (event.type == pygame.JOYBUTTONUP):
                button = self.buttonName(event.button, scheme)
                self.readButton(button, joy, scheme["button"], map)
                changed = True
            elif event.type == pygame.JOYAXISMOTION:
                axis = self.axisName(event.axis, scheme)
                self.readAxis(axis, joy, scheme["axis"], map)
                changed = True
            elif event.type == pygame.JOYHATMOTION:
                hat = event.hat
                self.readHat(hat, joy, scheme, map)
                changed = True
            elif event.type == pygame.JOYDEVICEREMOVED :
                print("controller disconnected")
        while len(self.buttonSet) > 0:
            button = self.buttonSet.pop()
            if button < 15:
                self.updateButton(button, gamepad, modes[0], scheme["button"])
        while len(self.axisSet) > 0:
            axis = self.axisSet.pop()
            if axis < 6:
                self.updateAxis(axis, gamepad, modes[1], scheme["axis"])
        if changed:
            self.updateController(self.virtcon, self.activeMode[0], self.activeMode[1])
            
    def updatepart(self, scheme:dict[str, dict[str, int]], map:dict[str, any], modes:list[str]):
        self.updatefull(self.joyce, self.virtcon, scheme, map, modes)
    def update(self):
        self.updatefull(joy=self.joyce, gamepad=self.virtcon, scheme=self.activeScheme, map=self.activeMap, modes=self.activeMode)

    # print the current controller values
    def printController(self, control:dict[str, any]):
        for i in control:
            for j in control[i]:
                print(i + ":" + str(j) + " = " + str(control[i][j]))

    # changes the active scheme
    def setScheme(self, newscheme:dict[str, dict[str, bool]]):
        self.activeScheme = newscheme

    # changes the active scheme, usful for activly remaping the controller
    def setMap(self, newmap:dict[str, any]):
        self.activeMap = newmap

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
    # converts button input to axis input
    def cnvrtBtnToAxs(self, val:bool, keymap:dict):
        s = self.con["axis"][keymap['key']]
        v = keymap['val']
        if val:
            v = self.clampf(v + s)
        else:
            if self.sign(s) == self.sign(v):
                v = 0.0
            else:
                v = s
        return v

    # convert axis input to button
    def cnvrtAxsToBtn(self, val:float, keymap:dict):
        if self.sign(keymap['val']) == 1:
            return val > keymap['val']
        else:
            return val < keymap['val']

    # convert hat to button
    def cnvrtHatToBtn(self, val:int, keymap:dict):
        return val == keymap['val']

    # convert hat to axis
    def cnvrtHatToAxs(self, val:float, keymap:dict):
        val = 0
        if self.sign(keymap['val']) == 1.0:
            val = max(0.0, val)
        elif self.sign(keymap['val']) == -1.0:
            val = min(0.0, val)
        return val

    # return 1 or -1 if pos or neg, unless n = zero then returns 0
    def sign(self, n:float):
        try:
            return n/abs(n) 
        except ZeroDivisionError:return 0
    
    # locks value to between -1 and 1
    def clampf(self, n: float):
        return max(min(1, n), -1)
    
    # locks up or down. vert should be -1 or 1
    def upOrDown(n: float, vert: int):
        return max(min(1, vert*n), 0)

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
            return self.INPUTOPTIONS[ind]
        else:
            return 'null'
    def indexFromButtonStr(self, st: str):
        return self.INPUTOPTIONS.index(st)

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
    
    # returns the name of the button in the scheme
    def buttonName(self, ind: int, scheme:dict[str, dict[str, int]]):
        for i in scheme["button"].keys():
            if (scheme["button"][i] == ind):
                return i
        return "null"

    # returnd the name of the axis
    def axisName(self, ind: int, scheme:dict[str, dict[str, int]]):
        for i in scheme["axis"].keys():
            if (scheme["axis"][i] == ind):
                return i
        return "null"

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
        code = self.code['button'][self.strFromButtonIndex(key)]
        joy = self.con['button'][self.strFromButtonIndex(key)]
        if mode == 'or':
            return code | joy
        elif mode == 'xor':
            return (~code & joy) | (code & ~joy)
        elif mode == 'and':
            return code & joy
        elif mode == 'rand':
            r = random.randint(0,1) == 1
            return (code & r) | (joy & ~r)
        elif mode == 'joy':
            return joy
        elif mode == 'code':
            return code

    # returns a float based on both inputs and the combination method
    def combineAxis(self, key: int, mode: str) -> float:
        code = self.code['axis'][self.strFromAxisIndex(key)]
        joy = self.con['axis'][self.strFromAxisIndex(key)]
        if mode == 'max':
            if abs(code) > abs(joy):
                return code
            else: 
                return joy
        elif mode == 'min':
            if abs(code) > abs(joy):
                return joy
            else: 
                return code
        elif mode == 'joy':
            return joy
        elif mode == 'code':
            return code
        elif mode == "avg":
            return (code + joy) / 2

##################################################
##################### main #######################
cmap = [PS4SCHEME, PS4DEMOMAP]

if __name__ == '__main__':
    cntr = HybridController(cmap[0], cmap[1]) 
    cntr.setModes(["xor","max"])
    # this is a simple loop, and can be replaced by calling update() if this code is called from another file
    coderunning = True
    while coderunning:
        # sets a framerate
        cntr.pg.time.Clock().tick(60)
        # updates the system
        #cntr.updatefull(joy=cntr.joyce, gamepad=cntr.virtcon, scheme=PS4SCHEME, map=PS4DEFAULTMAP, modes=["joy","joy"]) 
        cntr.update()
        
