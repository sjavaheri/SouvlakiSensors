# import brickpi3
from utils.brick import Motor

BP = brickpi3.BrickPi3()

# initiate motors
# motor = Motor("A")
# other_motor = Motor("B")

MOTOR = BP.PORT_A

BP.set_motor_limits(MOTOR, 80, 720)

# reset position
# BP.reset_encoder(MOTOR)


# function to calculate degrees of rotations needed to achieve desired distance
def move(self, dist):
    Omega = (distance * 360) / (2 * 3.14159 * rw)


# get wanted distance in meters from user
distance = 0.9
rw = 0.042 / 2

# make the motors move
BP.set_motor_position_relative(MOTOR, ((distance * 360) / (2 * 3.1415926535 * rw)))
