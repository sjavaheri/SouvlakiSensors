#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors
import time

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=100)
TOUCH_SENSOR = TouchSensor(1)
SLEEP_TIME = 0.1

wait_ready_sensors() # Note: Touch sensors actually have no initialization time


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
            if TOUCH_SENSOR.is_pressed():
                print("Touch sensor has been pressed")
                # call play sound function
                play_sound()
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        BP.reset_all()  # reset all before exiting program
        exit()


if __name__=='__main__':
    play_sound()

    # TODO Implement this function
    play_sound_on_button_press()
