import brickpi3
from utils.brick import Motor

BP = brickpi3.BrickPi3()

# initiate motors
# motor = Motor("A")
# other_motor = Motor("B")

MOTOR = BP.PORT_A

BP.set_motor_limits(MOTOR, 80, 720)

# reset position
# BP.reset_encoder(MOTOR)

# make the motors move
BP.set_motor_position_relative(MOTOR, 60)

BP.set_motor_position_relative(MOTOR, 120)

BP.set_motor_position_relative(MOTOR, 180)

BP.set_motor_position_relative(MOTOR, 240)

BP.set_motor_position_relative(MOTOR, 300)

BP.set_motor_position_relative(MOTOR, 360)
