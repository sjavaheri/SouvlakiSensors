
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
SPEED = 140

# brick pi instance
BP = brickpi3.BrickPi3()

# drum motor
drumMotor = Motor("B")
drum = BP.PORT_B
maxPowerDrum = 80
maxSpeedDrum = 270

# infinite while loop for running the drum
# uses threading to be able to start and stop a while loop from within another one

stopDrumsFlag = threading.Event()

def drummingLoop(): 
    while not stopDrumsFlag: 
        if debug:
            print("drumsPlaying")
        
        time.sleep(DRUM_TIME) 
        drumMotor.set_position(0)
        time.sleep(DRUM_TIME)
        exit()
    
    return

if __name__=='__main__':

    # motor setup 
    try: 
        # drum
        BP.offset_motor_encoder(drum, BP.get_motor_encoder(drum))
        drumMotor.set_limits(maxPowerDrum, maxSpeedDrum)
        drumMotor.set_power(0)
    except IOError as error:

        if debug: 
            print("Motor initialization failed due to error : ", error)
        BP.reset_all()
        exit()

# variables for start stop subsystem
stop = False
drumsOn = False
up = True
counter = 0
# create thread for drums
drumsThread = threading.Thread(target=drummingLoop)

# infinite polling loop for musical instrument
while True:
    try: 
        #control polling rate the musical instrument
        time.sleep(DRUM_TIME)


        # prevent any other behaviour if stop == true, and stop the drums
        # will loop back up until stop becomes true again
        if (stop == True): 
            # TODO: Add function call to stop the drums
            if drumsOn: 
                # stop drums 
                drumsOn = False 
            continue
        
        if drumsOn:
            # counter to control that drumming polling rate is slower than polling rate of machine
            counter = counter + 1
            if (counter % 50 == 0):
                # reset counter 
                counter = 0 
                # move drum arm either up or down
                if (up): 
                    up = False
                    drumMotor.set_position(90)
                else: 
                    up = True
                    drumMotor.set_position(-2)
            




                
    
    except BaseException as e:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        BP.reset_all()  # reset all before exiting program
        print(e)
        exit()  
