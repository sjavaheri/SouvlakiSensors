
"""
Code for the music playing robot 
""" 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors
import time
import brickpi3
import threading

debug = True

# polling time of the robot
SLEEP_TIME = 0.01
DRUM_TIME = 1

# brick pi instance
BP = brickpi3.BrickPi3()

# drum motor
drum = BP.PORT_B
maxPowerDrum = 80
maxSpeedDrum = 270

# infinite while loop for running the drum
# uses threading to be able to start and stop a while loop from within another one

stopDrumsFlag = threading.Event()

def drummingLoop(): 
    while not stopDrumsFlag: 
        # do the drum motions
        drum.set_power(maxPowerDrum)
        drum.set_position_relative(60)
        drum.set_power(0)
        time.sleep(DRUM_TIME)
    return

if __name__=='__main__':

    # motor setup 
    try: 
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
stop = False
startDrumming = False
drumsPlaying = False

# create thread for drums
drumsThread = threading.Thread(target=drummingLoop)

# infinite polling loop for musical instrument
while True:
    try: 
        #control polling rate the musical instrument
        time.sleep(SLEEP_TIME)

        startDrumming = True

        # prevent any other behaviour if stop == true, and stop the drums
        # will loop back up until stop becomes true again
        if (stop == True): 
            # TODO: Add function call to stop the drums
            if (drumsPlaying): 
                # stop drum thread gracefully
                stopDrumsFlag.set()
                drumsThread.join()
                drumsPlaying = False
            continue
        
        if (startDrumming and (not drumsPlaying)): 
            drumsThread.start()
        
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        BP.reset_all()  # reset all before exiting program
        exit()  
