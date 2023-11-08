# Software Subsystem Code
# Authors: Shidan Javaheri, Alice Godbout

# import statements
from utils.brick import (
    EV3ColorSensor,
    wait_ready_sensors,
    SensorError,
    reset_brick,
    Motor,
)
import brickpi3
import time
import random

# import selection code
from selection import *
from deployment import *


# Data Structures for Software Subsystem
# --------------------------------------

# state of the city. Represented by 4 * 4 matrix of 0s.
# fire code : Types A - F Represented by integers 1 - 6
debug = True
city_map = [[0 for _ in range(4)] for _ in range(4)]
current_bearing = 0
current_position = (3, 0)
state = ""


if __name__ == "__main__":
    """
    Main function of the tests
    """
    # brick pi instance
    BP = brickpi3.BrickPi3()

    # Initialize Input Sensors
    # ------------------------
    # Initialize Motors
    # -----------------

    # selection motor
    selection_port = BP.PORT_C
    selection_motor = Motor("C")

    max_power_select = 40
    max_speed_select = 50

    # deployment motor
    deployment_port = BP.PORT_D
    deployment_motor = Motor("D")

    max_power_deploy = 40
    max_speed_deploy = 150

    # setup all motors
    try:
        # selection_motor
        BP.offset_motor_encoder(selection_port, BP.get_motor_encoder(selection_port))
        BP.set_motor_limits(selection_port, max_power_select, max_speed_select)
        BP.set_motor_power(selection_port, 0)

        # deployment_motor
        BP.offset_motor_encoder(deployment_port, BP.get_motor_encoder(deployment_port))
        BP.set_motor_limits(deployment_port, max_power_deploy, max_speed_deploy)
        BP.set_motor_power(deployment_port, 0)

    except IOError as error:
        if debug:
            print("Motor initialization failed due to error : ", error)
        BP.reset_all()
        exit()

    while True:
        try:
            # display loading instructions
            state = "loading"
            if debug: 
                print(state)
            time.sleep(2)

            # get user input
            state = "inputting"
            if debug: 
                print(state)
            time.sleep(2)

            state = "moving"
            if debug: 
                print(state)
            time.sleep(2)

            state = "selecting"
            if debug: 
                print(state)

            # test that I can select all the cubes, no matter their order
            tests = [2,4,6,1,3,5]
            print("normal")
            for fire_number in tests: 
                select_fire_suppressant(fire_number, selection_motor, selection_port)
                deploy_fire(deployment_motor)
                if debug:
                    print(fire_number)
                time.sleep(5)
            time.sleep(10)
            
            # randomly scramble the list and do it again
            random.shuffle(tests)
            print("random no1")
            for fire_number in tests: 
                select_fire_suppressant(fire_number, selection_motor, selection_port)
                deploy_fire(deployment_motor)
                if debug:
                    print(fire_number)
                time.sleep(5)
            time.sleep(10)
            
            # randomly scramble the list and do it again
            random.shuffle(tests)
            print("random no2")
            for fire_number in tests: 
                select_fire_suppressant(fire_number, selection_motor, selection_port)
                deploy_fire(deployment_motor)
                if debug:
                    print(fire_number)
                time.sleep(5)
            time.sleep(10)
            
            # randomly scramble the list and do it again
            random.shuffle(tests)
            print("random no3")
            for fire_number in tests: 
                select_fire_suppressant(fire_number, selection_motor, selection_port)
                deploy_fire(deployment_motor)
                if debug:
                    print(fire_number)
                time.sleep(5)
            time.sleep(10)
            
            # randomly scramble the list and do it again
            random.shuffle(tests)
            print("random no4")
            for fire_number in tests: 
                select_fire_suppressant(fire_number, selection_motor, selection_port)
                deploy_fire(deployment_motor)
                if debug:
                    print(fire_number)
                time.sleep(5)
            
            BP.reset_all()
            exit()
            
        # capture all exceptions
        except BaseException:
            BP.reset_all()  # reset all before exiting program
            exit()
