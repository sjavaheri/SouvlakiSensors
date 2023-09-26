#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, SensorError
import csv
import time 


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"
SLEEP_TIME = 0.1
# complete this based on your hardware setup
EV3ColorSensor = EV3ColorSensor(2)
TouchSensor = TouchSensor(1)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data(debug=False):
    "Collect color sensor data."
    # open the csv file to write data to it row by row (overwrites other data)
    csvFile = open(COLOR_SENSOR_DATA_FILE, "w")

    # stores the current state of the touch sensor (true if pressed, false otherwise)
    state = False
    counter = 0

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
                # write to csv file
                csvFile.write('{:d}, {:d}, {:d}\n'.format(red, green, blue))
                # print results to console
                if (debug):
                    print("\nTrigger Number: ",counter,". See data below: \n")
                    print("Red: ", red, "Green: ", green, "Blue: ", blue, "\n")
                # sleep for 0.1 seconds
                time.sleep(SLEEP_TIME)
                status = False
            else: 
                time.sleep(SLEEP_TIME)
        # catch any errors 
        except SensorError as e: 
            print("There was an error from the sensor: ", e)
        except KeyboardInterrupt: 
                print("Keyboard Interrupt. Exiting program.")
        finally:
            csvFile.close()
            print("CSV file closed.")

if __name__ == "__main__":
    collect_color_sensor_data(debug=True)
