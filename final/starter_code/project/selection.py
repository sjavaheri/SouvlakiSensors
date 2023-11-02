# Selection Subsystem Code
# Authors: Shidan Javaheri, Alice Godbout

from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors
import time
import brickpi3

debug = True
BP = brickpi3.BrickPi3()

# Main Function for Selection Subsystem
# --------------------------------
def select_fire_suppressant(fire_type, selection_motor):
    """
    Based on the type of fire at this location, select the appropriate fire suppressant

    Args:
        fire_type (int): type of fire at this location
        selection_motor (Motor): selection motor

    Returns:
        None

    Mapping:
        Letter  Color    Integer     Position
        D       Red      4           0
        E       Orange   5           60
        B       Yellow   2           120
        F       Green    6           180
        A       Blue     1           240
        C       Purple   3           300

    """

    # check / test if it is better to get position with get_motor_encoder or by updating current position variable
    absolutePosition = BP.get_motor_encoder(selection_motor)
    current_position = absolutePosition % 360

    mapping = {1: 240, 2: 120, 3: 300, 4: 0, 5: 60, 6: 180}

    desired_position = mapping[fire_type]

    # relative move required
    relative_move = (desired_position - current_position) % 360

    # if relative move is greater than 180, move counterclockwise
    if relative_move > 180:
        relative_move -= 360

    # set motor to new relative position
    selection_motor.set_position_relative(relative_move)

    return
