 #!/usr/bin/env python3

"""
Code for the Note Playing Subsystem
Adapts the code from lab 2 to play a different note for each touch sensor that is pressed. 

"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors
import time
import brickpi3

SLEEP_TIME = 0.01

debug = True

# touch sensors
tSensor1 = TouchSensor(1)
tSensor2 = TouchSensor(2)
tSensor3 = TouchSensor(3)
tSensor4 = TouchSensor(4)

# sounds
sound1 = sound.Sound(duration=0.3, pitch="C4", volume=100)
sound2 = sound.Sound(duration=0.3, pitch="D4", volume=100)
sound3 = sound.Sound(duration=0.3, pitch="E4", volume=100)
sound4 = sound.Sound(duration=0.3, pitch="F4", volume=100)

BP = brickpi3.BrickPi3() # create an instance of the BrickPI3 

# wait for sensors to be ready
wait_ready_sensors() # Note: Touch sensors actually have no initialization time
print("Touch sensors ready")   

# play a single note
def play_sound(SOUND):
    "Play a single note."
    SOUND.play()
    SOUND.wait_done()


def notePlaying():
    "In an infinite loop, play a single note when the touch sensor is pressed."
    try:
        while True:
            #control polling rate the musical instrument
            time.sleep(SLEEP_TIME)

            # poll touch sensors
            if (tSensor1.is_pressed()):
                if (debug): print("Touch sensor 1 has been pressed")
                # call play sound function
                play_sound(sound1)
                
            # check if touch sensor 2 is pressed
            if (tSensor2.is_pressed()):
                if (debug): print("Touch sensor 2 has been pressed")
                # call play sound function
                play_sound(sound2)
            
            # check if touch sensor 3 is pressed
            if (tSensor3.is_pressed()):
                if (debug): print("Touch sensor 3 has been pressed")
                # call play sound function
                play_sound(sound3)
            
            # check if touch sensor 4 is pressed
            if (tSensor4.is_pressed()):
                if (debug): print("Touch sensor 4 has been pressed")
                # call play sound function
                play_sound(sound4)

            
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        BP.reset_all()  # reset all before exiting program
        exit()


if __name__=='__main__':

    # TODO Implement this function
    notePlaying()