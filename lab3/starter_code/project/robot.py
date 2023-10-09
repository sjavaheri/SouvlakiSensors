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

# startStop motor
startStop = BP.PORT_A
maxPowerStartStop = 0 
maxSpeedStartStop = 0

# drum motor
drum = BP.PORT_B
maxPowerDrum = 80
maxSpeedDrum = 270

# wait for sensors to be ready
wait_ready_sensors() # Note: Touch sensors actually have no initialization time
if (debug): print("Touch sensors ready")   

# play a single note
def play_sound(SOUND):
    "Play a single note."
    SOUND.play()
    # ensures that two sounds can be played together, which we want for flute like behaviour
    SOUND.wait_done()


if __name__=='__main__':

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
stop = False
startDrumming = False
drumsPlaying = False
# infinite polling loop for musical instrument
while True:
    try: 
        #control polling rate the musical instrument
        time.sleep(SLEEP_TIME)

        # poll emergency stop - has priority so comes first
        # get position of motor (% 360 just in case. Build will restrict motion of switch)
        absolutePosition =  BP.get_motor_encoder(startStop)
        position = absolutePosition % 360
        # position of emergency stop
        if (position <= 290 and position >= 250): 
            stop = True
            if (debug): print(position, "stop")
        # position of start drumming
        elif (position >= 70 and position <= 110):
            startDrumming = True
            if (debug): print(position, "start")
        # stop has not been triggered
        else: 
            stop = False
            if (debug): print(position, "nothing")

        # prevent any other behaviour if stop == true, and stop the drums
        # will loop back up until stop becomes true again
        if (stop == True): 
            # TODO: Add function call to stop the drums
            # if (drumsPlaying): 
                # stop drums if they are playing 
                # drumsPlaying = False
            continue
        
        # TODO: Add code here to start playing drums
        # if (drumsPlaying = False and startDrumming = True): 
            # start the drums
            # drumsPlaying = True

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
