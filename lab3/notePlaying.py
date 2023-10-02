 #!/usr/bin/env python3

"""
Code for the Note Playing Subsystem
Adapts the code from lab 2 to play a different note for each touch sensor that is pressed. 

"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors
import time

tSensor1 = TouchSensor(1)
tSensor2 = TouchSensor(2)

SLEEP_TIME = 0.05

wait_ready_sensors() # Note: Touch sensors actually have no initialization time
print("Touch sensors ready")   


def play_sound():
    "Play a single note."
    SOUND.play()
    SOUND.wait_done()


def play_sound_on_button_press():
    "In an infinite loop, play a single note when the touch sensor is pressed."
    try:
        while True:
            #control polling rate of touch sensor 
            time.sleep(SLEEP_TIME)
            # check if touch sensor is pressed
            if (tSensor1.is_pressed()):
                #play the C note
                sound1 = sound.Sound(duration=0.3, pitch="C4", volume=100)
                print("Touch sensor 1 has been pressed")
                # call play sound function
                play_sound()
                # loop until the button is no longer pressed
                while (tSensor1.is_pressed()):
                    time.sleep(SLEEP_TIME)
                    play_sound()
            if (tSensor2.is_pressed()):
                #play the D note
                sound2 = sound.Sound(duration=0.3, pitch="D4", volume=100)
                print("Touch sensor 2 has been pressed")
                # call play sound function
                play_sound()
                # loop until the button is no longer pressed
                while (tSensor2.is_pressed()):
                    time.sleep(SLEEP_TIME)
                    play_sound()
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        BP.reset_all()  # reset all before exiting program
        exit()


if __name__=='__main__':

    # TODO Implement this function
    play_sound_on_button_press()