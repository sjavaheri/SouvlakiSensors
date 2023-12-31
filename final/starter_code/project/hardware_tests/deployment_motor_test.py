# Unit Test for the Deployment Subsystem
# Authors: Alice Godbout, Sara Andari

import brickpi3
from project.utils.brick import Motor

BP = brickpi3.BrickPi3()

# initiate motors
MOTOR = BP.PORT_A

BP.set_motor_limits(MOTOR, 100, 180)

# make the motors move
BP.set_motor_position_relative(MOTOR, 360)
