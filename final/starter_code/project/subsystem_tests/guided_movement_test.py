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

# other subystem code
from movement import *
from selection import *
from deployment import *

# Data Structures for Software Subsystem
# --------------------------------------

# state of the city. Represented by 4 * 4 matrix of 0s.
# fire code : Types A - F Represented by integers 1 - 6
debug = True
city_map = [[0 for _ in range(4)] for _ in range(4)]
current_bearing = 0
current_position = (0, 0)
state = ""


def wait_for_sensors(c1, c2):
    """
    Waits for the sensors to be ready
    """
    # example from brick pi 2
    test_left_cs = 0
    test_right_cs = 0
    while test_left_cs == 0 and test_right_cs == 0:
        try:
            test_left_cs = BP.get_sensor(c1.port)
            test_right_cs = BP.get_snesor(c2.port)
        except:
            time.sleep(0.05)

    # built in function
    wait_ready_sensors()
    print("System Boot Successful. The Exterminator is ready to exterminnate!")
    return

if __name__ == "__main__":
    """
    Main function of the softawre subsystem
    """
    # brick pi instance
    BP = brickpi3.BrickPi3()

    # Initialize Input Sensors
    # ------------------------

    # color sensors
    # color sensor 39
    color_sensor_right = EV3ColorSensor(1)
    color_sensor_left = EV3ColorSensor(3)

    # Initialize Motors
    # -----------------

    # left wheel
    left_wheel_port = BP.PORT_A
    left_wheel = Motor("A")

    # right wheel
    right_wheel_port = BP.PORT_B
    right_wheel = Motor("B")

    max_power_wheels = 40
    max_speed_wheels = 50

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
        # left_wheel_motor
        BP.offset_motor_encoder(left_wheel_port, BP.get_motor_encoder(left_wheel_port))
        BP.set_motor_limits(left_wheel_port, max_power_wheels, max_speed_wheels)
        BP.set_motor_power(left_wheel_port, 0)

        # right_wheel_motor
        BP.offset_motor_encoder(
            right_wheel_port, BP.get_motor_encoder(right_wheel_port)
        )
        BP.set_motor_limits(right_wheel_port, max_power_wheels, max_speed_wheels)
        BP.set_motor_power(right_wheel_port, 0)

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

    # wait for sensors to be ready
    wait_for_sensors(color_sensor_left, color_sensor_right)
    count = 0
    while True:
        
        try:

            # Test 1 - Right Squares - Succeeds

            move_forward(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
            cross_green(right_wheel, left_wheel, color_sensor_right, color_sensor_left, SPEED = -200, DELTA = -20)
            turn_right(right_wheel, left_wheel, color_sensor_right, color_sensor_left) 
            count += 1


            # Test 2 - Left Squares - Succeeds

            # move_forward(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
            # cross_green(right_wheel, left_wheel, color_sensor_right, color_sensor_left, SPEED = -200, DELTA = -20)
            # turn_left(right_wheel, left_wheel, color_sensor_right, color_sensor_left) 
            # count += 1

            # Test 3 - Reverse - Fails (DO NOT DO THIS)

            # move_forward(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
            # cross_green_reverse(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
            # reverse(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
            # cross_green(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
            # count += 1

            if (count > 10): 
                BP.reset_all()
                break

        # capture all exceptions
        except BaseException:
            BP.reset_all()  # reset all before exiting program
            exit()
