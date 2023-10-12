"""
Code for the music playing robot 
"""
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors
import time
import brickpi3

debug = True

# polling time of the robot
SLEEP_TIME = 0.01

# brick pi instance
BP = brickpi3.BrickPi3()

# configure touch sensors

# configure sounds for touch sensors

# startStop motor
startStop = BP.PORT_A
maxPowerStartStop = 0
maxSpeedStartStop = 0

# configure drum motor

# wait for sensors to be ready

# any functions needed by main code go here

if __name__ == "__main__":
    # motor setup
    try:
        # start stop
        BP.offset_motor_encoder(startStop, BP.get_motor_encoder(startStop))
        BP.set_motor_limits(startStop, maxPowerStartStop, maxSpeedStartStop)
        BP.set_motor_power(startStop, 0)

        # drum motor setup

    except IOError as error:
        if debug:
            print("Motor initialization failed due to error : ", error)
        BP.reset_all()
        exit()

# variables for start stop subsystem
stop = False
startDrumming = False
drumsPlaying = False
# infinite polling loop for musical instrument
while True:
    try:
        # control polling rate the musical instrument
        time.sleep(SLEEP_TIME)

        # poll emergency stop - has priority so comes first
        # get position of motor (% 360 just in case. Build will restrict motion of switch)
        
        # test: changed positions for start, stop, nothing
        
        absolutePosition = BP.get_motor_encoder(startStop)
        position = absolutePosition % 360
        # position of emergency stop
        if position <= 290 and position >= 250:
            stop = True
            if debug:
                print(position, "stop")
        # position of start drumming
        elif position >= 70 and position <= 110:
            startDrumming = True
            if debug:
                print(position, "start")
        # stop has not been triggered
        else:
            stop = False
            if debug:
                print(position, "nothing")

        # prevent any other behaviour if stop == true, and stop the drums
        # will loop back up until stop becomes true again
        if stop == True:
            # TODO: Add function call to stop the drums
            # if (drumsPlaying):
            # stop drums if they are playing
            # drumsPlaying = False
            continue

        # TODO: Add code here to start playing drums
        # if (drumsPlaying = False and startDrumming = True):
        # start the drums. May require threading for a seperate while loop
        # drumsPlaying = True

        # TODO: Poll touch sensors

    except (
        BaseException
    ) as e:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print(f"Error occured : {e}")
        BP.reset_all()  # reset all before exiting program
        exit()
