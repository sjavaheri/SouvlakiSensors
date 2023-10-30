# Movement Subsystem Code 
# Authors: Shidan Javaher, Alice Godbout
from collections import deque
import math

# Data Structures for Movement Subsystem
# --------------------------------------

# color tables: normalized values [red, green, blue, color], for colors red, green, blue, and other
colorTable39 = [[0.742003,0.187976,0.070021, "red"], [0.189534, 0.646703, 0.163763, "green"], [0.267834, 0.437618,0.294547, "blue"], 
                [0.493422,0.39193,0.114648, "other"]]

colorTable40 = [[0.755809, 0.146725, 0.097466, "red"], [0.19179, 0.579413, 0.228797, "green"], [0.26186, 0.342986, 0.395153, "blue"], 
                [0.50464, 0.334221, 0.16114, "other"]]

# Global Variables for Movement Subsytem
# --------------------------------------
SPEED = 150
DELTA = 20
SAMPLING_RATE = 0.2

# Main Functions for Movement Subsystem
# --------------------------------

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

def move_forward(right_wheel, left_wheel,color_sensor_right, color_sensor_left): 
    """
    Move robot forward until both color sensors read green

    Error: if any color sensor reads red or blue

    Args: 
        right_wheel (Motor): right wheel motor
        left_wheel (Motor): left wheel motor
        color_sensor_right (ColorSensor): color sensor 39
        color_sensor_left (ColorSensor): color sensor 40
    
    Returns:
        None
    """
    while True: 
        
        # get the readings of the two color sensors
        r,g,b = color_sensor_right.get_value()
        


    return 

def reverse(current_position, current_bearing):
    """
    Reveres the robot to the square it just came from, after deployment

    Args: 
        current_position (tuple): current position of the robot
        current_bearing (int): current bearing of the robot

    Returns: 
        tuple: current position of the robot
    """


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








