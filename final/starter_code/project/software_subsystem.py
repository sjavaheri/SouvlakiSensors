# Software Subsystem Code
# Authors: Shidan Javaher, Alice Godbout

# import statements
from utils.brick import EV3ColorSensor, wait_ready_sensors, SensorError, reset_brick, Motor
import brickpi3

# other subystem code
from movement_subsystem import *
from selection_subsystem import *
from deployment_subsystem import *

# Data Structures for Software Subsystem
# --------------------------------------

# state of the city. Represented by 4 * 4 matrix of 0s. 
# fire code : Types A - F Represented by integeres 1 - 6
debug = True
city_state = [[0 for _ in range(4)] for _ in range(4)]
current_bearing = 0 
current_position = (0,0)
state = ""

def wait_for_sensors(c1, c2):
    """
    Waits for the sensors to be ready
    """
    # example from brick pi 2
    test_left_cs = 0 
    test_right_cs = 0
    while (test_left_cs == 0 and test_right_cs ==0): 
        try: 
            test_left_cs = BP.get_sensor(c1.port)
            test_right_cs = BP.get_snesor(c2.port)
        except: 
            time.sleep(0.05)

    # built in function
    wait_ready_sensors()
    print("System Boot Successful. The Exterminator is ready to exterminnate!")
    return

# TODO

def display_loading_instructions(): 
    """
    Displays instructions for how to load the robot. Asks user to enter yes when loading is complete
    """
    return

def get_user_input(): 
    """
    Gets the user input for the fire coordinates
    Convert coordinates into proper coordinates for array 
    User will input (x,y). We will not adjust the values

    Format: x1,y1,LETTER1,x2,y2,LETTER,x3,y3,LETTER3

    Returns:
        list : a list of tuples representing the fire coordinates, in order of increasing distance from the starting position 0,0
    """
    return 


if __name__ == '__main__':
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
    color_sensor_left = EV3ColorSensor(2)

    # Initialize Motors
    # -----------------

    # left wheel
    left_wheel_port = BP.PORT_A
    left_wheel = Motor("A")

    # right wheel
    right_wheel_port = BP.PORT_B
    right_wheel = Motor("B")

    max_power_wheels = 40
    max_speed_wheels = 150

    # selection motor
    selection_port = BP.PORT_C
    selection_motor = Motor("C")

    max_power_select = 40
    max_speed_select = 150

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
        BP.offset_motor_encoder(right_wheel_port, BP.get_motor_encoder(right_wheel_port))
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

    while True: 
        try: 

            # move_forward(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
            # time.sleep(1)
            # crossGreen(right_wheel, left_wheel, color_sensor_right, color_sensor_left, SPEED = -200, DELTA = -20)
            # time.sleep(1)
            # reverse(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
            time.sleep(1)
            turn_blind(right_wheel, left_wheel)
            time.sleep(1)
            turn_blind(right_wheel, left_wheel)
            time.sleep(1)
            turn_blind(right_wheel, left_wheel)
            time.sleep(1)
            turn_blind(right_wheel, left_wheel)
            break
            # state = "Loading"
            # # display loading instructions
            # display_loading_instructions()
            # state = "Inputting"

            # # get user input to set fire locations
            # fire_coordinates = get_user_input()
            # state = "moving"

            # # now we are ready for the robot to move to the desired location
            # for x,y in fire_coordinates: 

            #     # move to fire
            #     current_position, current_bearing = move_to_point(x, y, city_state, current_position, current_bearing, left_wheel, right_wheel, color_sensor_right, color_sensor_left); 
            #     state = "selecting"

            #     # select fire suppressant
            #     select_fire_suppressant(city_state[x][y], selection_motor)
            #     state = "deploying"

            #     # deploy fire suppressant
            #     deploy_fire(deployment_motor)
            #     state = "reversing"

            #     # reverse
            #     current_position = reverse(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
            #     state = "moving"

            # # go home
            # current_position, current_bearing = move_to_point(0, 0, city_state, current_position, current_bearing, right_wheel, left_wheel, color_sensor_right, color_sensor_left)

            # # reorient to have forward facing bearing
            # # use turn function

        # capture all exceptions
        except BaseException:
            BP.reset_all()  # reset all before exiting program
            exit()




        











