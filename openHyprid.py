# this is a demonstration of how to use the code
import ControllerCodeHybridizer
import time
import vgamepad

# lists all avalable input names
inputOptions = ['a', 'b', 'x', 'y', 'back', 'guide', 'start', 'left thumb', 'right thumb', 'left shoulder', 'right shoulder', 'dpad up', 'dpad down', 'dpad left', 'dpad right', 'left stick x', 'left stick y', 'right stick x', 'right stick y', 'left trigger','right trigger']

# you need a scheme that matches your controller in order for it to work. as well as needing to set the combination modes
# if you dont want to creat one manually just run the createScheme.py code
PS4SCHEME = {'button':{'x':0, 'circle':1, 'square':2, 'triangle':3, 'share':4, 'guide':5, 'options':6, 'left thumb':7, 'right thumb':8, 'left shoulder':9, 'right shoulder':10, 'dpad up':11, 'dpad down':12, 'dpad left':13, 'dpad right':14, 'track pad':15}, 
            "axis":{'left stick x':0, 'left stick y':1, 'right stick x':2, 'right stick y':3, 'left trigger':4, 'right trigger':5}}
# it is nessisary to have a map that determines how inputs are converted to xbox inputs.
# varrying the map can allow 
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

# creating new modes of combination can give you more control over how the code interacts with the natural inputs for example: making specific buttons only work for the controller or the code
modes = ['and','sum']

# in its initialization it needs to know the scheme and mapping
con = ControllerCodeHybridizer.HybridController(PS4SCHEME, PS4DEFAULTMAP)
# if you dont set a mode it defualts to ["joy", "joy"]
con.setModes(modes)

control = con.virtcon
control.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
control.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
c = vgamepad.VX360Gamepad()
c.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
c.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
c1 = vgamepad.VX360Gamepad()
c1.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
c1.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
c2 = vgamepad.VX360Gamepad()
c2.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
c2.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
con.connectToController("PS4 controller")

# simple loop
tick = 0
while True:
    # sets the code side of the controller to a random state 
    con.randomize()
    # avoids calling 3 problamatic buttons
    con.setButtonInt(4, False) #back
    con.setButtonInt(5, False) #guide
    con.setButtonInt(6, False) #start

    # actually updates the values of the virtual controler based on if the input has changed
    con.update()

    # loops at a framerate
    time.sleep(1/60)
    tick+=1
    tick+=1
