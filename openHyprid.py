# this is a demonstration of how to use the code
import ControllerCodeHybridizer
import time

# lists all avalable input names
inputOptions = ['a', 'b', 'x', 'y', 'back', 'guide', 'start', 'left thumb', 'right thumb', 'left shoulder', 'right shoulder', 'dpad up', 'dpad down', 'dpad left', 'dpad right', 'left stick x', 'left stick y', 'right stick x', 'right stick y', 'left trigger','right trigger']

# you need a scheme that matches your controller in order for it to work. as well as needing to set the combination modes
# if you dont want to creat one manually just jun the createScheme.py code
PS4SCHEME = {'button':{'a':0, 'b':1, 'x':2, 'y':3, 'back':4, 'guide':5, 'start':6, 'left thumb':7, 'right thumb':8, 'left shoulder':9, 'right shoulder':10, 'dpad up':11, 'dpad down':12, 'dpad left':13, 'dpad right':14, 'track pad':15}, 'axis':{'left stick x':0, 'left stick y':1, 'right stick x':2, 'right stick y':3, 'left trigger':4, 'right trigger':5}}
# creating new modes of combination can give you more control over how the code interacts with the natural inputs for example: making specific buttons only work for the controller or the code
modes = ['and','max']

# in its initialization it needs to know the scheme
con = ControllerCodeHybridizer.HybridController(PS4SCHEME)
# if you dont set a mode it defualts to ["joy", "joy"]
con.setModes(modes)

# simple loop
tick = 0
while True:
    # avoids calling 3 problamatic buttons
    if not (inputOptions[tick%15] in ['back','guide','start']):
        # sets a button to true
        con.setButton(tick%15, True)
    # sets a button to false
    con.setButton((tick+8)%15, False)
    # sets an axis to some float (in this case -1,0,1)
    con.setAxis((tick%17)%6, (tick%5)%3-1)

    # actually updates the values of the virtual controler based on if the input has changed
    con.update()

    # loops at a framerate
    time.sleep(1/60)
    tick+=1