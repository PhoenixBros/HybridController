###################################################################
# this code is a bit outdated, but still gives valuable information
###################################################################


# mostly stolen from https://stackoverflow.com/questions/46506850/how-can-i-get-input-from-an-xbox-one-controller-in-python
# modified to create the scheme and map them output all inputs
import pygame
import time
pygame.init()
joysticks = []
clock = pygame.time.Clock()
keepPlaying = True

# stuff to make it easier for you to make a scheme
buttonOptions = ['a', 'b', 'x', 'y', 'back', 'guide', 'start', 'left thumb', 'right thumb', 'left shoulder', 'right shoulder', 'dpad up', 'dpad down', 'dpad left', 'dpad right']
axisOptions = ['left stick x', 'left stick y', 'right stick x', 'right stick y', 'left trigger','right trigger']
current = 0
scheme = {"button":{},"axis":{}}
once = False

# do you want to create a scheme
createScheme = True

# automating the mapping prosses is hard. i might try again later
# createMapping

# for all the connected joysticks
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    print ("Detected joystick ", joysticks[-1].get_name())


while keepPlaying:
    clock.tick(60)
    if not once:
        once = True
        if current < len(buttonOptions):
            print(buttonOptions[current])
        elif current-len(buttonOptions) < len(axisOptions):
            print(axisOptions[current-len(buttonOptions)])
        else:
            createScheme = False
            once = False
    for event in pygame.event.get((pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION, pygame.JOYBALLMOTION)):
        if createScheme:
            if current < len(buttonOptions):
                if event.type == pygame.JOYBUTTONDOWN:
                    if not (event.button in scheme["button"].values()):
                        print(event)
                        scheme["button"][buttonOptions[current]] = event.button
                        once = False
                        current +=1
            elif current-len(buttonOptions) < len(axisOptions):
                if event.type == pygame.JOYAXISMOTION:
                    if abs(event.value) > .5:
                        if not (event.axis in scheme["axis"].values()):
                            print(event)
                            scheme["axis"][axisOptions[current-len(buttonOptions)]] = event.axis
                            once = False
                            current += 1
        else:
            if not once:
                print("\nHere is a usable scheme. simply copy and past it as a new scheme to initialise ControllerCodeHybridizer.py\nMYSCHEME =" ,scheme, "\n\nfrom here on it will display the number for the input you put")
                once = True
                time.sleep(2)
                pygame.event.clear()
            if event.type == pygame.JOYAXISMOTION:
                if abs(event.value) > .5:
                    print(event)
            else:
                print(event)
