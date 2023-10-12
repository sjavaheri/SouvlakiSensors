
"""
Code for the music playing robot
"""
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, Motor
import time
import brickpi3
import threading

debug = True

# polling time of the robot
SLEEP_TIME = 0.01
DRUM_TIME = 1

# brick pi instance
BP = brickpi3.BrickPi3()


# startStop motor
startStop = BP.PORT_A
startMotor = Motor("A")
maxPowerStartStop = 0
maxSpeedStartStop = 0

# drum motor
drumMotor = Motor("B")
drum = BP.PORT_B
maxPowerDrum = 40
maxSpeedDrum = 150

# global variables for drum motor
up = True
stop = False

# wait for sensors to be ready
wait_ready_sensors()  # Note: Touch sensors actually have no initialization time
if (debug):
    print("Touch sensors ready")

# open a file to write the strike data
file = open("strike_data.csv", "w")
# close file 
file.close()



if __name__ == '__main__':

    # motor setup
    try:
        # start stop
        BP.offset_motor_encoder(startStop, BP.get_motor_encoder(startStop))
        BP.set_motor_limits(startStop, maxPowerStartStop, maxSpeedStartStop)
        BP.set_motor_power(startStop, 0)

        # drum
        BP.offset_motor_encoder(drum, BP.get_motor_encoder(drum))
        BP.set_motor_limits(drum, maxPowerDrum, maxSpeedDrum)
        BP.set_motor_power(drum, 0)
    except IOError as error:

        if debug:
            print("Motor initialization failed due to error : ", error)
        BP.reset_all()
        exit()

# variables for start stop subsystem
drums_on = False
# time variable for drum polling
old_time = time.time()


# infinite polling loop for musical instrument
while True:
    try:
        # control polling rate the musical instrument
        time.sleep(SLEEP_TIME)

        # poll emergency stop - has priority so comes first

        # get position of motor (% 360 just in case. Build will restrict motion of switch)
        absolutePosition = BP.get_motor_encoder(startStop)
        position = absolutePosition % 360
        # position of emergency stop
        if (position <= 290 and position >= 250):
            stop = True
            drums_on = False

        # position of start drumming
        elif (position >= 70 and position <= 110):
            drums_on = True 
           
        # stop has not been triggered
        else:
            stop = False

        # Emergency stop 
        if (stop == True): 
            # TODO: Add function call to stop the drums
            if drums_on: 
                # stop drums 
                drums_on = False 
            continue
        
        # drumming functionality
        if drums_on:
            # counter to control that drumming polling rate is slower than polling rate of machine
            if (time.time() - old_time > 1):
                # move drum arm either up or down
                if (up): 
                    up = False
                    drumMotor.set_position(-45)
                    # open file and write to it
                    file = open("strike_data.csv", "a")
                    file.write(str(time.time()-old_time) + "\n")
                    file.close()

                else: 
                    up = True
                    drumMotor.set_position(2)
                    # open file and write to it
                    file = open("strike_data.csv", "a")
                    file.write(str(time.time()-old_time) + "\n")
                    file.close()

                old_time = time.time()

    # capture all exceptions including KeyboardInterrupt (Ctrl-C)
    except BaseException:
        BP.reset_all()  # reset all before exiting program
        exit()
