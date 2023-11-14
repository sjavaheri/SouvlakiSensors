# Movement Subsystem Code 
# Authors: Shidan Javaher, Alice Godbout
from collections import deque
import math
import time
import brickpi3
debug = True
# Data Structures for Movement Subsystem
# --------------------------------------

# color tables: normalized values [red, green, blue, color], for colors red, green, blue, and other
colorTable39 = [[0.742003,0.187976,0.070021, "red"], [0.189534, 0.646703, 0.163763, "green"], [0.267834, 0.437618,0.294547, "blue"], 
                [0.493422,0.39193,0.114648, "other"]]

colorTable40 = [[0.755809, 0.146725, 0.097466, "red"], [0.19179, 0.579413, 0.228797, "green"], [0.26186, 0.342986, 0.395153, "blue"], 
                [0.50464, 0.334221, 0.16114, "other"]]

# Global Variables for Movement Subsytem
# --------------------------------------
BP = brickpi3.BrickPi3()
SPEED = 200
DELTA = 160
WHEEL_DIAMETER = 0.043
AXLE_LENGTH = 0.17
ORIENT_TO_DEG = AXLE_LENGTH/WHEEL_DIAMETER
DIST_TO_DEG = 180 / (math.pi * (WHEEL_DIAMETER/2))
DEG_TO_DIST = (math.pi * (WHEEL_DIAMETER / 2))/180
SAMPLING_RATE = 0.05
TURN_SPEED = 200
debug = True


# Main Functions for Movement Subsystem
# --------------------------------
# TODO: After Unit Testing

def move_to_point(destination, city_map, current_position, current_bearing, right_wheel, left_wheel, color_sensor_right, color_sensor_left, home = False): 
    """
    Moves the robot to a point on the city grid, so that it can deploy the fire suppressant

    Args: 
        point (tuple): point on the city grid to move to
        city_state (list): 4x4 matrix representing the city
        current_position (tuple): current position of the robot
        current_bearing (int): current bearing of the robot
        left_wheel (Motor): left wheel motor
        right_wheel (Motor): right wheel motor
        color_sensor_39 (ColorSensor): color sensor 39
        color_sensor_40 (ColorSensor): color sensor 40
        home (bool): whether the robot is returning home or not

    Returns:
        tuple: current position of the robot
        int: current bearing of the robot
        tuple: the last point the robot visited before arriving at the destination
    """
    start_x, start_y = current_position
    x, y = current_position
    end_x, end_y = destination
    
    # get the path to the point
    path = shortest_path(city_map, x, y, end_x, end_y)
    if debug: 
        print("The path is: ", path)
    
    last_point = False
    # move to each point in the path
    for next_x, next_y in path: 
        
        if (next_x, next_y) == (end_x, end_y):
            last_point = True
        if debug: 
            print("Moving to point: ", next_x, next_y)
            print("Current Bearing: ", current_bearing)
            
        # move to the next point
        # find if I need to turn left or right - (DX AND DY SWAPPED to due array - map relation)
        dx = next_y - y
        dy = x - next_x
        
        if debug: 
            print("Change dx, dy: " + str(dx) + ", " +  str(dy))
        # Cover all possibilities of movement
        
        # move right along x
        if (dx == 1 and dy == 0):       
            # check current bearing
            if (current_bearing == 0):
                turn_blind(90, right_wheel, left_wheel)
            elif (current_bearing == 180): 
                turn_blind(-90, right_wheel, left_wheel)
            elif (current_bearing == 270):
                turn_blind(180, right_wheel, left_wheel)
            current_bearing = 90

        # move left along x
        elif (dx == -1 and dy == 0):
            if (current_bearing == 0):
                turn_blind(-90, right_wheel, left_wheel)
            elif (current_bearing == 90): 
                turn_blind(180, right_wheel, left_wheel)
            elif (current_bearing == 180):
                turn_blind(90, right_wheel, left_wheel)
            current_bearing = 270

        # move up along y
        elif (dx == 0 and dy == 1):
            if (current_bearing == 90):
                turn_blind(-90, right_wheel, left_wheel)
            elif (current_bearing == 180): 
                turn_blind(180, right_wheel, left_wheel)
            elif (current_bearing == 270):
                turn_blind(90, right_wheel, left_wheel)
            current_bearing = 0

        
        # move down along y
        elif (dx == 0 and dy == -1):
            if (current_bearing == 0):
                turn_blind(180, right_wheel, left_wheel)
            elif (current_bearing == 90): 
                turn_blind(90, right_wheel, left_wheel)
            elif (current_bearing == 270):
                turn_blind(-90, right_wheel, left_wheel)
            current_bearing = 180
            
        if debug:   
            print("New current bearing: ", current_bearing)
            
        # move forward off green
        move_forward_blind(0.055, right_wheel, left_wheel)
        
        # move forward to next green
        move_forward(right_wheel, left_wheel, color_sensor_right, color_sensor_left, current_bearing)
        
        if (not last_point): 
            # adjust for next turn
            move_forward_blind(0.045, right_wheel, left_wheel)
        
        # reverse to get chute in good position
        if (last_point and not home):
            move_backward_blind(0.02,right_wheel, left_wheel)
        
        if (last_point and home): 
            move_forward_blind(0.045,right_wheel, left_wheel)
            
        # adjust current point 
        x, y = next_x, next_y
        
    
    # return current position and bearing, and second last element in path
    last_point_on_path = 0 
    if (len(path)>1): 
        last_point_on_path = path[-2]
    else: 
        last_point_on_path = (start_x, start_y)
    
    return (end_x, end_y), current_bearing, last_point_on_path
             


# Guided Functions
# --------------------------------

def move_forward(right_wheel, left_wheel,color_sensor_right, color_sensor_left, current_bearing, SPEED=SPEED, DELTA=DELTA): 
    """
    Move robot forward until both color sensors are green

    Error: if any color sensor reads red or blue. Fixed by turning on the spot

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40
    
    Returns:
        None
    """
    # loop until destination reached
    error_counter = 0
    # initial_rotation = BP.get_motor_encoder(BP.PORT_A)
    # distance = 0.18
    while True: 
        
        # get the readings of the two color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        rl,gl,bl = color_sensor_left.get_rgb()
        color_right = classifyColor(39, rr, gr, br)
        color_left = classifyColor(40, rl, gl, bl)
        

        # error correction
        if ((current_bearing == 0 or current_bearing == 180) and color_right == "blue"): 
            color_right = "green"

        if debug: 
            print("Left Color: ", color_left, "Right Color: ", color_right)

        # check if destination is reached
        if (color_right == "green" and color_left == "green"): 
            # if its the first iteration, cross the green
            left_wheel.set_dps(0)
            right_wheel.set_dps(0)
            return

        # # determine if the error is to the left or right. Stop error correction after distance cm
        # error = "none"
        # if (BP.get_motor_encoder(BP.PORT_A) - initial_rotation > distance * DIST_TO_DEG): 
        #     print("no more correcting")
        #     error = "none"
        error = "none"
        if ((color_left == "red" or color_left == "blue") and not (color_left == "green" or color_right =="green")): 
            error_counter += 1
            if (error_counter >= 2):
                error_counter = 0
                error = "left"
        elif ((color_right == "red" or color_right == "blue") and not (color_right == "green" or color_left =="green")):         
            error_counter += 1
            if (error_counter >= 2):
                error_counter = 0
                error = "right"
        else:
            error = "none"
            error_counter = 0
        
        # ITERATION 1 - adjust the motors based on the error

        # if error is to the left, turn right
        # if (error == "left"): 
        #     left_wheel.set_dps(SPEED - (DELTA))
        #     right_wheel.set_dps(SPEED + DELTA)
        # elif (error == "right"): 
        #     left_wheel. set_dps(SPEED + DELTA)
        #     right_wheel.set_dps(SPEED - (DELTA))
        # else:
        #     left_wheel.set_dps(SPEED)
        #     right_wheel.set_dps(SPEED)
        
        # ITERATION 2 - turn on the pot to fix the error
        if (error == "left"): 
           correct_turn(error, right_wheel, left_wheel,color_sensor_right, color_sensor_left, SPEED, DELTA)
        elif (error == "right"): 
            correct_turn(error, right_wheel, left_wheel,color_sensor_right, color_sensor_left, SPEED, DELTA)
        else:
            left_wheel.set_dps(SPEED)
            right_wheel.set_dps(SPEED)

        time.sleep(SAMPLING_RATE)


def correct_turn(error, right_wheel, left_wheel,color_sensor_right, color_sensor_left, SPEED=SPEED, DELTA=DELTA): 
    """
    Turn robot on the spot to remove the error

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40
    
    Returns:
        None
    """
    # set the direciton of the turn based on the error
    if (error == "left"): 
        left_wheel.set_dps(SPEED)
        right_wheel.set_dps(-SPEED)
    elif (error == "right"): 
        left_wheel.set_dps(-SPEED)
        right_wheel.set_dps(SPEED)
        
    while True: 
        if debug: 
            print("correcting") 
            
        # get the readings of the two color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        rl,gl,bl = color_sensor_left.get_rgb()
        color_right = classifyColor(39, rr, gr, br)
        color_left = classifyColor(40, rl, gl, bl)

        # if debug: 
        #     print("Left Color: ", color_left, "Right Color: ", color_right)

        # check if error has been removed
        if (color_right == "other" and color_left == "other"): 
            # if its the first iteration, cross the green
            left_wheel.set_dps(0)
            right_wheel.set_dps(0)
            return
        
        # handle extreme cases - turned too far so that the other sensor is no longer on other
        # fix by pulsing the other motor briefly before returning
        # move_forward function will call correct turn again, and pulse will have helped it be able to correct       
        if (error == "left" and not(color_right == "other")): 
            right_wheel.set_dps(SPEED)
            left_wheel.set_dps(0)
            time.sleep(0.4)
            right_wheel.set_dps(0)
            return
        
        elif (error == "right" and not (color_left == "other")): 
            right_wheel.set_dps(0)
            left_wheel.set_dps(SPEED)
            time.sleep(0.4)
            left_wheel.set_dps(0)
            return  
     
        time.sleep(SAMPLING_RATE)


def guided_180(right_wheel, left_wheel,color_sensor_right, color_sensor_left, SPEED=SPEED, DELTA=DELTA): 
    """
    Guided 180 degree turn on the spot. Turn 90 degrees, then keep turning looking for the line for the city street

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40
    
    Returns:
        None
    """
    # turn 90 blind 
    turn_blind(90, right_wheel, left_wheel)
    passedOnce = False

    rr,gr,br = color_sensor_right.get_rgb()
    rl,gl,bl = color_sensor_left.get_rgb()
    color_right = classifyColor(39, rr, gr, br)
    color_left = classifyColor(40, rl, gl, bl)
    
    # fix error when both color sensors have same value. It is safe to move forward a little bit
    if ((color_left == "blue" and color_right == "blue") or (color_left =="red" and color_right == "red")): 
        move_forward_blind(0.012, right_wheel, left_wheel)
    elif (color_left == "other" and color_right == "other"): 
        move_backward_till_line(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
        move_forward_blind(0.012, right_wheel, left_wheel)
        
    # loop until turn complete
    left_wheel.set_dps(-SPEED)
    right_wheel.set_dps(SPEED)
    
    while True: 
        
        # get the readings of the two color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        rl,gl,bl = color_sensor_left.get_rgb()
        color_right = classifyColor(39, rr, gr, br)
        color_left = classifyColor(40, rl, gl, bl)
        
        if debug: 
            print("Colors while turning: left: ",color_left, "right: ", color_right)
        
        if (color_right == "red" or color_right == "blue"): 
            passedOnce = True
        # color sensor has passed over the city street line
        if (passedOnce and (color_right == "other" or (color_right != "other" and color_left != "other"))): 
            left_wheel.set_dps(0)
            right_wheel.set_dps(0)
            return
     
        time.sleep(SAMPLING_RATE)


def move_backward_till_line(right_wheel, left_wheel,color_sensor_right, color_sensor_left, SPEED=SPEED, DELTA=DELTA): 
    """
    Turn robot on the spot to remove the error

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40
    
    Returns:
        None
    """
    # set the direciton of the turn based on the error
    
    left_wheel.set_dps(-SPEED)
    right_wheel.set_dps(-SPEED)
    
    while True: 
        if debug: 
            print("correcting") 
            
        # get the readings of the two color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        rl,gl,bl = color_sensor_left.get_rgb()
        color_right = classifyColor(39, rr, gr, br)
        color_left = classifyColor(40, rl, gl, bl)

        # if debug: 
        #     print("Left Color: ", color_left, "Right Color: ", color_right)

        # check if error has been removed
        if (not (color_right == "other") or not (color_left == "other")): 
            # if its the first iteration, cross the green
            left_wheel.set_dps(0)
            right_wheel.set_dps(0)
            return
        
        time.sleep(SAMPLING_RATE)

        
def reverse( right_wheel, left_wheel, color_sensor_right, color_sensor_left, current_bearing): 
    """
    Reverse after a cube has been deployed to the previous intersection
    """
    move_backward_blind(0.13, right_wheel, left_wheel)
    # move_forward_short(0.20, right_wheel, left_wheel, color_sensor_right, color_sensor_left) 
    # move_backward_blind(0.15, right_wheel, left_wheel)
    # move_forward_short(0.15, right_wheel, left_wheel, color_sensor_right, color_sensor_left) 
    # move_backward_blind(0.225, right_wheel, left_wheel)
    # reverse_guided(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
    guided_180(right_wheel, left_wheel, color_sensor_right, color_sensor_left)
    move_forward(right_wheel, left_wheel, color_sensor_right, color_sensor_left, current_bearing)
    move_forward_blind(0.05, right_wheel, left_wheel)


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
    left_wheel.set_position_relative(-int(angle*0.96* ORIENT_TO_DEG))
    right_wheel.set_position_relative(int(angle *0.96*ORIENT_TO_DEG))
    wait_for_motor(right_wheel)
    print("inside turn")



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
        colorTable = colorTable40
    elif (id == 40):
        colorTable = colorTable39
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



# ITERATION 1 - GUIDED FUNCTIONS THAT DIDN'T WORK
# -----------------------------------------------------------------------

def align(color_right, color_left,right_wheel, left_wheel,color_sensor_right, color_sensor_left, SPEED=SPEED, DELTA=DELTA): 
    """
    move one wheel forward until that color sensor sees green

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40
    
    Returns:
        None
    """
    # loop until destination reached
    if ((color_left == "green") and not (color_right == "green")): 
        right_wheel.set_dps(SPEED)
        left_wheel.set_dps(0)
    elif(not (color_left == "green ") and (color_right == "green")): 
        left_wheel.set_dps(SPEED)
        right_wheel.set_dps(0)
    else: 
        return
    while True: 
        if debug: 
            print("aligning")
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

        time.sleep(SAMPLING_RATE)

def move_forward_short(distance, right_wheel, left_wheel,color_sensor_right, color_sensor_left, SPEED=SPEED, DELTA=DELTA): 
    """
    Move robot forward guided by sensors until time finishes

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
    print("here")
    # get the port of the left motor
    initial_rotation = BP.get_motor_encoder(BP.PORT_A)
    print(initial_rotation)
    while True: 
        
        # get the readings of the two color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        rl,gl,bl = color_sensor_left.get_rgb()
        color_right = classifyColor(39, rr, gr, br)
        color_left = classifyColor(40, rl, gl, bl)

        # if debug: 
        #     print("Left Color: ", color_left, "Right Color: ", color_right)

        # check if distance is reached
        print(distance * DIST_TO_DEG)
        if (BP.get_motor_encoder(BP.PORT_A) - initial_rotation > distance * DIST_TO_DEG): 
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
        # if debug: 
        #     print("The current error is: ", error)
        
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


def reverse_guided(right_wheel, left_wheel, color_sensor_right, color_sensor_left):
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
        if (start > 15): 
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
        if (error == "left" and count < 3): 
            left_wheel.set_dps(-SPEED + DELTA)
            right_wheel.set_dps(-SPEED - DELTA)
            
        elif (error == "right" and count < 3): 
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
    
    right_wheel.set_dps(-SPEED)
    while True: 
        
        # get the readings of the left color sensors
        rr,gr,br = color_sensor_right.get_rgb()
        color_right = classifyColor(39, rr, gr, br) 

        # turn to get left sensor off green
        if (color_right != "green"):  
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





