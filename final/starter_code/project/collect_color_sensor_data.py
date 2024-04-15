#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, SensorError, reset_brick
import csv
import time 
import math 


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"
SLEEP_TIME = 0.1
# complete this based on your hardware setup
EV3ColorSensor = EV3ColorSensor(3)
TouchSensor = TouchSensor(4)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data(debug=False, classify=False):
    "Collect color sensor data."
    # open the csv file to clear it of contents / create it. Close it afterwards (later will be opened in append mode)
    csvFile = open(COLOR_SENSOR_DATA_FILE, "w")
    csvFile.close()

    # stores the current state of the touch sensor (true if pressed, false otherwise)
    state = False
    counter = 0

    # ask user if they would like to test the classification algorithm. Loop until valid input is recieved
    validInput = False
    while (not validInput):
        decision = input("Would you like to test the classification algorithm? yes/no \n ").lower()
        if (decision == "yes"): 
            print("Classificaion test activated\n")
            validInput = True
            classify = True
        elif (decision == "no"):
            print("Classification test not activated")
            validInput = True
            classify = False
        else: 
            print ("Please enter a valid input: yes or no")

    while True: 
        try: 
            # sleep for 0.1 seconds
            time.sleep(SLEEP_TIME)
            
            # check if sensor is pressed
            state = TouchSensor.is_pressed()
            if (state == True): 
                counter = counter + 1
                # break down the r,g,b values
                red, green, blue = EV3ColorSensor.get_rgb()
                # open csv file and append results to it. Close afterwards                
                csvFile = open(COLOR_SENSOR_DATA_FILE, "a")
                csvFile.write('{:d}, {:d}, {:d}\n'.format(red, green, blue))
                csvFile.close()
                # print results to console
                if (debug):
                    print("\nTrigger Number: ",counter,". See data below: \n")
                    print("Red: ", red, "Green: ", green, "Blue: ", blue, "\n")
                # classify the color of the cube if requested
                if (classify): 
                    color = classifyColoredCube39(red, green, blue)
                    print("The color of the cube is: ", color)
                state = False
                # sleep for 0.1 seconds
                time.sleep(SLEEP_TIME)
            else: 
                time.sleep(SLEEP_TIME)
        # catch any errors 
        except SensorError as e: 
            print("There was an error from the sensor: ", e)
        except KeyboardInterrupt: 
            print("Keyboard Interrupt. Exiting program.")

# function to classify the color of a cube
def classifyColoredCube40(red, green, blue): 
    # color table: normalized values [red, green, blue, color], for colors red, green, blue, and other
    colorTable = [[0.755809, 0.146725, 0.097466, "red"], [0.19179, 0.579413, 0.228797, "green"], [0.26186, 0.342986, 0.395153, "blue"], 
                  [0.50464, 0.334221, 0.16114, "other"]]
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

# function to classify the color of a cube
def classifyColoredCube39(red, green, blue): 
    # color table: normalized values [red, green, blue, color], for colors red, green, blue, and other
    colorTable = [[0.742003,0.187976,0.070021, "red"], [0.189534, 0.646703, 0.163763, "green"], [0.267834, 0.437618,0.294547, "blue"], 
                  [0.493422,0.39193,0.114648, "other"]]
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

if __name__ == "__main__":
    collect_color_sensor_data(debug=True, classify=False)