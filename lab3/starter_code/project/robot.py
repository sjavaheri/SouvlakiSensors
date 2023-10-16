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

# global variables for drum motor
up = True
stop = False

# variables for start stop subsystem
drums_on = False

# play a single note
def play_sound(SOUND):
    "Play a single note."
    SOUND.play()
    # ensures that two sounds can be played together, which we want for flute like behaviour
    SOUND.wait_done()

# initialize touch sensors
touch_sensor1 = TouchSensor(1)
touch_sensor2 = TouchSensor(2)
touch_sensor3 = TouchSensor(3)
touch_sensor4 = TouchSensor(4)

# initialize sounds for each touch sensor
sound1 = sound.Sound(duration=0.3, pitch="C4", volume=100)
sound2 = sound.Sound(duration=0.3, pitch="D4", volume=100)
sound3 = sound.Sound(duration=0.3, pitch="E4", volume=100)
sound4 = sound.Sound(duration=0.3, pitch="F4", volume=100)

# initailize the startStop motor
start_stop = BP.PORT_A
start_motor = Motor("A")
max_power_start_stop = 0
max_speed_start_stop = 0

# initialize the drum motor
drum_motor = Motor("B")
drum = BP.PORT_B
max_power_drum = 40
max_speed_drum = 150


# wait for sensors to be ready
wait_ready_sensors()  # Note: Touch sensors actually have no initialization time
if (debug):
    print("Touch sensors ready")



# polling sensors in a seperate thread
def poll_sensors(): 
    while True: 

        # emergency stop
        if stop:
            continue

        # poll touch sensors
        if (touch_sensor1.is_pressed()):
            if (debug):
                print("Touch sensor 1 has been pressed")
            play_sound(sound1)

        # check if touch sensor 2 is pressed
        if (touch_sensor2.is_pressed()):
            if (debug):
                print("Touch sensor 2 has been pressed")
            play_sound(sound2)

        # check if touch sensor 3 is pressed
        if (touch_sensor3.is_pressed()):
            if (debug):
                print("Touch sensor 3 has been pressed")
            play_sound(sound3)

        # check if touch sensor 4 is pressed
        if (touch_sensor4.is_pressed()):
            if (debug):
                print("Touch sensor 4 has been pressed")
            play_sound(sound4)



if __name__ == '__main__':

    # motor setup
    try:
        # start stop
        BP.offset_motor_encoder(start_stop, BP.get_motor_encoder(start_stop))
        BP.set_motor_limits(start_stop, max_power_start_stop, max_speed_start_stop)
        BP.set_motor_power(start_stop, 0)

        # drum
        BP.offset_motor_encoder(drum, BP.get_motor_encoder(drum))
        BP.set_motor_limits(drum, max_power_drum, max_speed_drum)
        BP.set_motor_power(drum, 0)

    except IOError as error:

        if debug:
            print("Motor initialization failed due to error : ", error)
        BP.reset_all()
        exit()

# time variable for drum polling
old_time = time.time()

# thread for the polling of sensors
sensors = threading.Thread(target=poll_sensors, daemon = True)
# begin infinite polling of sensors
sensors.start()

# infinite polling loop for musical instrument
while True:
    try:
        # control polling rate the musical instrument
        time.sleep(SLEEP_TIME)

        # poll emergency stop - has priority so comes first

        # get position of motor (% 360 just in case. Build will restrict motion of switch)
        absolute_position = BP.get_motor_encoder(start_stop)
        position = absolute_position % 360
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
                    drum_motor.set_position(-45)
                    if debug: 
                        print("up")
                else: 
                    up = True
                    drum_motor.set_position(2)
            
                    if debug:
                        print("down")

                old_time = time.time()

    # capture all exceptions
    except BaseException:
        BP.reset_all()  # reset all before exiting program
        exit()
