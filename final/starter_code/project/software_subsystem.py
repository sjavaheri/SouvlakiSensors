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
current_position = (3, 0)
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


def display_loading_instructions():
    """
    Displays instructions for how to load the robot. Asks user to enter yes when loading is complete
    """
    # display instructions
    response = ""
    while response.lower() != "yes" and response.lower() != "y":
        response = input("\nWelcome! Please follow the following instructions to load our robot. \nDo you confirm you want to continue? ")
        
        if (response != "yes" and response != "y"):
            print("Invalid Input\n")

    print("\nPlace cubes according to the color displayed on the cardboard.\n")
    
    # ask the user to enter 'yes' once loading is complete
    loading_response = ""
    while loading_response.lower() != "yes" and loading_response.lower() != "y":
        loading_response = input("\nEnter 'yes' or 'y' when loading is complete: ")
        
        if (loading_response != "yes" and loading_response != "y"):
            print("Invalid Input")

    print("\nRobot loading confirmed. Proceed to the next step.")
    return 



def get_user_input():
    """
    Gets the user input for the fire coordinates
    Convert coordinates into proper coordinates for array
    
    User will input (x,y). We will convert them to coordinates on the array 
    (x,y) -> (3-y, x)

    Format: x1,y1,LETTER1,x2,y2,LETTER,x3,y3,LETTER3

    Returns:
        list : a list of tuples representing the fire coordinates, in order of increasing distance from the starting position 0,0

    """

    fire_input = input(
        "\nEnter the fire coordinates (Format: x1,y1,LETTER1,x2,y2,LETTER,x3,y3,LETTER3): "
    )

    # TODO : user input verification

    # split the input string at commas
    fire_list = []
    for i in range(0, len(fire_input.split(",")), 3):
        fire_list.append(fire_input.split(",")[i : i + 3])

    # convert letter (fire types) into integers
    fire_coords = []  # list containing only location
    fires = []  # list containing the location and types of fires
    for fire in fire_list:
        # convert coordinates into proper coordinates for array
        x = 3 - int(fire[1])
        y = int(fire[0])
        fire_type = ord(fire[2].upper()) - ord("A") + 1
        fire_coords.append((x, y))
        fires.append((x, y, fire_type))

    # sort fires by increasing distance from (0,0)
    sorted_coords = sorted(fire_coords, key=lambda x: ((x[0] - 3) ** 2 + x[1] ** 2) ** 0.5)

    # update city_map with fire types
    for x, y, fire_type in fires:
        city_map[x][y] = fire_type

    return sorted_coords


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
    left_wheel_port = BP.PORT_B
    left_wheel = Motor("B")

    # right wheel
    right_wheel_port = BP.PORT_A
    right_wheel = Motor("A")

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

    while True:
        try:
            # display loading instructions
            state = "loading"
            if debug: 
                print(state)
            display_loading_instructions()

            # get user input
            state = "inputting"
            fire_coordinates = get_user_input()
            print (fire_coordinates)
            print(city_map)

            # now we are ready for the robot to move to the desired location
            for point in fire_coordinates:
                state = "moving"
                if debug: 
                    print(state)
                # move to fire
                current_position, current_bearing, reverse_point = move_to_point(point,city_map, current_position, current_bearing, right_wheel,left_wheel, color_sensor_right, color_sensor_left)
                state = "selecting"
                
                if debug: 
                    print(state)
                time.sleep(2)

                # select fire suppressant
                # select_fire_suppressant(city_map[x][y], selection_motor)
                state = "deploying"
                if debug: 
                    print(state)
                time.sleep(2)

                # deploy fire suppressant
                # deploy_fire(deployment_motor)
                state = "reversing"
                if debug: 
                    print(state)

                # reverse
                reverse(right_wheel, left_wheel, color_sensor_right, color_sensor_left, current_bearing)
                # robot turned around by 180 during reversal
                current_position = reverse_point
                current_bearing = (current_bearing + 180) % 360
                if (debug):
                    print("Successfully reversed to: ", current_position)

            # go home
            current_position, current_bearing,reverse_point = move_to_point(
                (3,0),
                city_map,
                current_position,
                current_bearing,
                right_wheel,
                left_wheel,
                color_sensor_right,
                color_sensor_left,
                home = True
            )
            # reset the city state             
            city_map = [[0 for _ in range(4)] for _ in range(4)]

        # capture all exceptions
        except BaseException:
            BP.reset_all()  # reset all before exiting program
            exit()
