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
_ = EV3ColorSensor(1)
_ = TouchSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data(debug=False):
    "Collect color sensor data."
    # open the csv file to write data to it row by row (overwrites other data)
    with open(COLOR_SENSOR_DATA_FILE, "w",  newline='') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=',')

        # stores the current state of the touch sensor (true if pressed, false otherwise)
        state = False

        while True: 
            try: 
                # check if sensor is pressed
                state = TouchSensor.is_pressed()
                if (state == True): 
                    # break down the r,g,b values
                    red, green, blue = EV3ColorSensor.get_rgb()
                    # write to csv file
                    csvWriter.writerow([red, green, blue])
                    # print results to console
                    print("\nColor sensor triggered. See data below: \n")
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
                 csvFile.close()


if __name__ == "__main__":
    collect_color_sensor_data(True)
