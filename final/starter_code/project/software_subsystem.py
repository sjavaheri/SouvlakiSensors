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
# fire code : Types 1 - 6 Represented by integeres 1 - 6
debug = True
city_state = [[0 for _ in range(4)] for _ in range(4)]
current_bearing = 0 
current_position = (0,0)
state = ""

# motor setup
def setup_motor(port, max_power, max_speed):
    """
    Sets the properties of a motor
    
    Args: 
        port (int): Port number of the motor
        max_power (int): Maximum power of the motor
        max_speed (int): Maximum speed of the motor

    Returns:
        None
    """

    try:
        # set motor properties       
        BP.offset_motor_encoder(port, BP.get_motor_encoder(port))
        BP.set_motor_limits(port, max_power, max_speed)
        BP.set_motor_power(port, 0)

    except IOError as error:

        if debug:
            print("Motor initialization failed due to error : ", error)
        BP.reset_all()
        exit()

def wait_for_sensors():
    """
    Waits for the sensors to be ready
    """
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
    color_sensor_39 = EV3ColorSensor(1)
    color_sensor_40 = EV3ColorSensor(2)

    # Initialize Motors
    # -----------------

    # left wheel
    left_wheel_port = BP.PORT_A
    left_wheel = Motor("A")

    # right wheel
    right_wheel_port = Motor("B")
    right_wheel = BP.PORT_B

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
    for port in [left_wheel_port, right_wheel_port, selection_port, deployment_port]:
        setup_motor(port, max_power_wheels, max_speed_wheels)

    # wait for sensors to be ready
    wait_for_sensors()

    while True: 
        try: 
            state = "Loading"
            # display loading instructions
            display_loading_instructions()
            state = "Inputting"

            # get user input to set fire locations
            fire_coordinates = get_user_input()
            state = "moving"

            # now we are ready for the robot to move to the desired location
            for x,y in fire_coordinates: 

                # move to fire
                current_position, current_bearing = move_to_point(x, y, city_state, current_position, current_bearing, left_wheel, right_wheel, color_sensor_39, color_sensor_40); 
                state = "selecting"

                # select fire suppressant
                select_fire_suppressant(city_state[x][y], selection_motor)
                state = "deploying"

                # deploy fire suppressant
                deploy_fire(deployment_motor)
                state = "reversing"

                # reverse
                current_position = reverse(current_position, current_bearing)
                state = "moving"

            # go home
            current_position, current_bearing = move_to_point(0, 0, city_state, current_position, current_bearing, left_wheel, right_wheel, color_sensor_39, color_sensor_40)

            # reorient to have forward facing bearing
            # use turn function

        # capture all exceptions
        except BaseException:
            BP.reset_all()  # reset all before exiting program
            exit()




        











