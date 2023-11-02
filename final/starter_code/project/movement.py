# Movement Subsystem Code 
# Authors: Shidan Javaher, Alice Godbout
from collections import deque
import math
import time
# import brickpi3
import time

# Data Structures for Movement Subsystem
# --------------------------------------

# color tables: normalized values [red, green, blue, color], for colors red, green, blue, and other
colorTable39 = [[0.742003,0.187976,0.070021, "red"], [0.189534, 0.646703, 0.163763, "green"], [0.267834, 0.437618,0.294547, "blue"], 
                [0.493422,0.39193,0.114648, "other"]]

colorTable40 = [[0.755809, 0.146725, 0.097466, "red"], [0.19179, 0.579413, 0.228797, "green"], [0.26186, 0.342986, 0.395153, "blue"], 
                [0.50464, 0.334221, 0.16114, "other"]]

# Global Variables for Movement Subsytem
# --------------------------------------
# BP = brickpi3.BrickPi3()
SPEED = 200
DELTA = 170
WHEEL_DIAMETER = 0.043
AXLE_LENGTH = 0.17
ORIENT_TO_DEG = AXLE_LENGTH/WHEEL_DIAMETER
DIST_TO_DEG = 180 / (math.pi * (WHEEL_DIAMETER/2))
SAMPLING_RATE = 0.05
TURN_SPEED = 200
debug = True


# Main Functions for Movement Subsystem
# --------------------------------
# TODO: After Unit Testing

def move_to_point(x, y, city_state, current_position, current_bearing, right_wheel, left_wheel, color_sensor_right, color_sensor_left): 
    """
    Moves the robot to a point on the city grid, so that it can deploy the fire suppressant

    Args: 
        x (int): x coordinate of destination
        y (int): y coordinate of destination
        city_state (list): 4x4 matrix representing the city
        current_position (tuple): current position of the robot
        current_bearing (int): current bearing of the robot
        left_wheel (Motor): left wheel motor
        right_wheel (Motor): right wheel motor
        color_sensor_39 (ColorSensor): color sensor 39
        color_sensor_40 (ColorSensor): color sensor 40

    Returns:
        tuple: current position of the robot
        int: current bearing of the robot
    """
    return

# Guided Functions
# --------------------------------

def move_forward(right_wheel, left_wheel,color_sensor_right, color_sensor_left, SPEED=SPEED, DELTA=DELTA): 
    """
    Move robot forward until both color sensors are green

    Error: if any color sensor reads red or blue

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40
    
    Returns:
        None
    """
    # loop until destination reached
    while True: 
        
        # get the readings of the two color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        rl,gl,bl = color_sensor_left.get_rgb()
        color_right = classifyColor(39, rr, gr, br)
        color_left = classifyColor(40, rl, gl, bl)

        if debug: 
            print("Left Color: ", color_left, "Right Color: ", color_right)

        # check if destination is reached
        if (color_right == "green" and color_left == "green"): 
            # if its the first iteration, cross the green
            left_wheel.set_dps(0)
            right_wheel.set_dps(0)
            return
        
        # determine if the error is to the left or right 
        error = "none"
        if (color_left == "red" or color_left == "blue"): 
            error = "left"
        elif (color_right == "red" or color_right == "blue"):
            error = "right"
        else:
            error = "none"
        if debug: 
            print("The current error is: ", error)
        
        # adjust the motors based on the error

        # if error is to the left, turn right
        if (error == "left"): 
            left_wheel.set_dps(SPEED -DELTA)
            right_wheel.set_dps(SPEED + DELTA)
        elif (error == "right"): 
            left_wheel. set_dps(SPEED + DELTA)
            right_wheel.set_dps(SPEED - DELTA)
        else:
            left_wheel.set_dps(SPEED)
            right_wheel.set_dps(SPEED)

        time.sleep(SAMPLING_RATE)

def reverse(right_wheel, left_wheel, color_sensor_right, color_sensor_left):
    """
    Reverse the robot briefly, while correcting its trajectory

    Error: only correct trajectory briefly (correction backwards is terrible)

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40


    Returns: 
        tuple: current position of the robot
    
    """
    # loop until destination reached, but with backwards speed and delta
    left_wheel.set_dps(-SPEED)
    right_wheel.set_dps(-SPEED)
    count = 0
    start = 0
    while True: 
        start += 1
        if (start > 30): 
            return
        # get the readings of the two color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        rl,gl,bl = color_sensor_left.get_rgb()
        color_right = classifyColor(39, rr, gr, br)
        color_left = classifyColor(40, rl, gl, bl)

        if debug: 
            print("Reverse")
            print("Left Color: ", color_left, "Right Color: ", color_right)

        # check if destination is reached
        if (color_right == "green" and color_left == "green"): 
            # if its the first iteration, cross the green
            left_wheel.set_dps(0)
            right_wheel.set_dps(0)
            return
        
        # determine if the error is to the left or right 
        if (color_left == "red" or color_left == "blue"): 
            error = "left"
            count += 1
        elif (color_right == "red" or color_right == "blue"):
            error = "right"
            count += 1
        else:
            error = "none"
        if debug: 
            print("The current error is: ", error)
        
        # adjust the motors based on the error

        # if error is to the left, turn right
        if (error == "left" and count < 5): 
            left_wheel.set_dps(-SPEED + DELTA)
            right_wheel.set_dps(-SPEED - DELTA)
            
        elif (error == "right" and count < 5): 
            left_wheel. set_dps(-SPEED - DELTA)
            right_wheel.set_dps(-SPEED + DELTA)
        
        else:
            left_wheel.set_dps(-SPEED)
            right_wheel.set_dps(-SPEED)

        time.sleep(SAMPLING_RATE)

def cross_green(right_wheel, left_wheel, color_sensor_right, color_sensor_left, SPEED=SPEED, DELTA=DELTA):
    """
    Code to cross through a building that is not on fire

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40

    Returns:
        None
    """
    # loop until destination reached
    while True: 
        
        # get the readings of the two color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        rl,gl,bl = color_sensor_left.get_rgb()
        color_right = classifyColor(39, rr, gr, br)
        color_left = classifyColor(40, rl, gl, bl)

        if debug: 
            print("Left Color: ", color_left, "Right Color: ", color_right)

        # check if destination is reached
        if (color_right != "green" and color_left != "green"): 
            left_wheel.set_dps(0)
            right_wheel.set_dps(0)
            return
        
        # determine if the error is to the left or right 
        error = "none"
        if (color_left !="green"): 
            error = "left"
        elif (color_right == "green"):
            error = "right"
        else:
            error = "none"
        if debug: 
            print("The current error is: ", error)
        
        # adjust the motors based on the error

        # if error is to the left, turn right
        if (error == "left"): 
            left_wheel.set_dps(SPEED + DELTA)
            right_wheel.set_dps(SPEED - DELTA)
        elif (error == "right"): 
            left_wheel. set_dps(SPEED - DELTA)
            right_wheel.set_dps(SPEED + DELTA)
        else:
            left_wheel.set_dps(SPEED)
            right_wheel.set_dps(SPEED)

        time.sleep(SAMPLING_RATE)

def cross_green_reverse(right_wheel, left_wheel, color_sensor_right, color_sensor_left):
    """
    cross green in the reverse direction
    """ 
    cross_green(right_wheel, left_wheel, color_sensor_right, color_sensor_left, SPEED = -SPEED, DELTA = -0.6*DELTA)

def turn_left(right_wheel, left_wheel, color_sensor_right, color_sensor_left, SPEED=TURN_SPEED, DELTA=DELTA):
    """
    Function to turn the robot left. Works by reversing the left wheel slightly, and then advancing the right wheel

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40

    Returns:
        None
    """ 
    while True: 
        
        # get the readings of the left color sensors
        rl,gl,bl = color_sensor_left.get_rgb()
        color_left = classifyColor(40, rl, gl, bl) 

        # turn to get left sensor off green
        if (color_left == "green"): 
            left_wheel.set_dps(-SPEED)
        else: 
            left_wheel.set_dps(0)
            break
        time.sleep(SAMPLING_RATE)

    # loop to position right wheel for turn
    was_in_green = False
    while True: 
        # get the readings of the right color sensor
        rr,gr,br = color_sensor_right.get_rgb()
        color_right = classifyColor(39, rr, gr, br)

        # get right wheen back to green
        if (color_right == "green"): 
            was_in_green = True
        else: 
            right_wheel.set_dps(SPEED)
        
        # turn to get right wheel across green
        if (was_in_green and color_right != "green"): 
            right_wheel.set_dps(0)
            break
        else: 
            right_wheel.set_dps(SPEED)

        time.sleep(SAMPLING_RATE)
    
    # adjust left wheel until it is on green
    while True: 
        left_wheel.set_dps(-SPEED)
        rl,gl,bl = color_sensor_left.get_rgb()
        color_left = classifyColor(40, rl, gl, bl) 
        if (color_left == "green"):
            left_wheel.set_dps(0)
            break
        time.sleep(SAMPLING_RATE)

    # check if both sensors are green, and advance off of it
    rl,gl,bl = color_sensor_left.get_rgb()
    color_left = classifyColor(40, rl, gl, bl) 
    rr,gr,br = color_sensor_right.get_rgb()
    color_right = classifyColor(39, rr, gr, br)
    if (color_left == "green" and color_right == "green"): 
        cross_green(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
    return

def turn_right(right_wheel, left_wheel, color_sensor_right, color_sensor_left, SPEED=TURN_SPEED, DELTA=DELTA):
    """
    Function to turn the robot right. Works by reversing the right wheel slightly, and then advancing the left wheel

    Args:
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40

    Returns:
        None
    """
    while True: 
        
        # get the readings of the left color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        color_right = classifyColor(39, rr, gr, br) 

        # turn to get left sensor off green
        if (color_right == "green"): 
            right_wheel.set_dps(-SPEED)
        else: 
            right_wheel.set_dps(0)
            break
        time.sleep(SAMPLING_RATE)

    # loop to position left wheel for turn
    was_in_green = False
    while True: 
        # get the readings of the right color sensor
        rl,gl,bl = color_sensor_left.get_rgb()
        color_left = classifyColor(40, rl, gl, bl)

        # get right wheen back to green
        if (color_left == "green"): 
            was_in_green = True
        else: 
            left_wheel.set_dps(SPEED)
        
        # turn to get right wheel across green
        if (was_in_green and color_left != "green"): 
            left_wheel.set_dps(0)
            break
        else: 
            left_wheel.set_dps(SPEED)

        time.sleep(SAMPLING_RATE)

    # adjust right wheel until it is on green
    while True: 
        right_wheel.set_dps(-SPEED)
        rr,gr,br = color_sensor_right.get_rgb()
        color_right = classifyColor(39, rr, gr, br) 
        if (color_right == "green"):
            right_wheel.set_dps(0)
            break
        time.sleep(SAMPLING_RATE)

    # check if both sensors are green, and advance off of them
    rl,gl,bl = color_sensor_left.get_rgb()
    color_left = classifyColor(40, rl, gl, bl) 
    rr,gr,br = color_sensor_right.get_rgb()
    color_right = classifyColor(39, rr, gr, br)
    if (color_left == "green" and color_right == "green"): 
        cross_green(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
    return


# Blind Functions
# -------------------------------- 

def wait_for_motor(motor): 
    """
    Wait for a motor to finish rotating

    Args: 
        motor (Motor) : the motor

    Returns: 
        None
    """
    while BP.get_motor_status(motor.port)[3] == 0 : 
        time.sleep(SAMPLING_RATE)
    while BP.get_motor_status(motor.port)[3] != 0 :
        time.sleep(SAMPLING_RATE)
        
def move_forward_blind(distance, right_wheel, left_wheel,SPEED=SPEED): 
    """
    Move robot forward blindly by a certain distance (in meters)

    Args: 
        distance (int): distance in meters
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        speed (int): speed of the motors
        delta (int): delta of the motors
    
    Returns:
        None
    """
    left_wheel.set_dps(SPEED)
    right_wheel.set_dps(SPEED)
    left_wheel.set_dps(SPEED)
    right_wheel.set_dps(SPEED)
    left_wheel.set_position_relative(int(distance * DIST_TO_DEG))
    right_wheel.set_position_relative(int(distance * DIST_TO_DEG))
    wait_for_motor(right_wheel)

def turn_blind(angle, right_wheel, left_wheel): 
    """
    Turn the robot blindly by an angle

    Args:
        angle (int): angle in degrees
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
    
    Returns:
        None
    """
    left_wheel.set_dps(SPEED)
    right_wheel.set_dps(SPEED)
    left_wheel.set_position_relative(int(angle*0.88 * ORIENT_TO_DEG))
    right_wheel.set_position_relative(-int(angle *0.88*ORIENT_TO_DEG))
    wait_for_motor(right_wheel)


def move_backward_blind(distance, right_wheel, left_wheel,SPEED=SPEED): 
    """
    Move robot backward a certain distance

    Args: 
        distance (int): distance
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
  
    Returns:
        None
    """
    left_wheel.set_dps(SPEED)
    right_wheel.set_dps(SPEED)
    left_wheel.set_position_relative(-int(distance * DIST_TO_DEG))
    right_wheel.set_position_relative(-int(distance * DIST_TO_DEG))
    wait_for_motor(right_wheel)



# Helper Functions for Movement Subsystem
# --------------------------------

# Functions to find shortest path to any vertex on the graph representing the city

def valid_point(x, y): 
    """
    Check if a point is valid on the city grid
    
    Args: 
        x (int): x coordinate
        y (int): y coordinate
    
    Returns:
        Boolean: True if point is valid, False otherwise
    """
    return x < 4 and x >= 0 and y < 4 and y >= 0

def shortest_path(graph, start_x, start_y, end_x, end_y): 
    """
    Find the shortest path from a point to another point on the city grid

    Uses a simple priority queue and bredth first search to find the shortest path

    Args:
        graph (list): 4x4 matrix representing the city
        start_x (int): x coordinate of starting point
        start_y (int): y coordinate of starting point
        end_x (int): x coordinate of ending point
        end_y (int): y coordinate of ending point

    Returns:
        list: list of tuples representing the shortest path from start to end
    """

    # queue stores current point being considered, and the path that was takent to reach the point
    priority_queue = deque([(start_x, start_y, [])])
    # keeps track of which points have been visited
    visited_points = set()

    while (priority_queue): 
        # deque and add point to visited set
        x, y , path = priority_queue.popleft()
        visited_points.add((x,y))

        # check if point is the target destination
        if (x == end_x and y == end_y): 
            return path
        
        # if this is not the target destination, try all possible movements
        # note - order of attempts biases priority
        # order of bias - right, up , left, down
        steps = [(1,0), (0,1), (-1,0), (0,-1)]

        for x_step, y_step in steps: 
            new_x, new_y = x + x_step, y + y_step
            dangerous = False 
            if (): 
                dangerous = True
            # check if point is valid | has not been visited | is not a fire unless its the target destination 
            if (valid_point(new_x, new_y) and ((new_x, new_y) not in visited_points) and (graph[new_x][new_y] == 0 or (new_x, new_y) == (end_x, end_y))): 
                # append new point to path
                new_path = path + [(new_x, new_y)]
                # add new point to queue
                priority_queue.append((new_x, new_y, new_path))

    return None


def classifyColor(id, red, green, blue): 
    """
    Classifies the color from an R G B reading of color sensor 39

    Args: 
        id (int): either 39 or 40
        red (int): red value
        green (int): green value
        blue (int): blue value

    Returns: 
        String: representing color of the block
    """
    # select color table based on id
    if (id == 39):
        colorTable = colorTable39
    elif (id == 40):
        colorTable = colorTable40
    else:
        return "invalid id"
    
    # store color and shortest distance
    currentColor = ''
    shortestDistance = 9999999

    # iterate through all colors and calculate the euclidean distance of the datapoint from the mean r g b values
    for i in range(0,4): 
        sum = red + green + blue
        distance = math.sqrt(((red/sum) - colorTable[i][0])**2 + ((green/sum) - colorTable[i][1])**2 + ((blue/sum) - colorTable[i][2])**2)
        # update if shorter distance found
        if (distance < shortestDistance): 
            shortestDistance = distance
            currentColor = colorTable[i][3]
    return currentColor







