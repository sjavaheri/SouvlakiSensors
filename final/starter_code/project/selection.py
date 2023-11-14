# Selection Subsystem Code
# Authors: Shidan Javaheri, Alice Godbout

from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors
import time
import brickpi3

debug = True
done_before = False
BP = brickpi3.BrickPi3()
SAMPLING_RATE=0.2

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

# Main Function for Selection Subsystem
# --------------------------------
def select_fire_suppressant(fire_type, selection_motor, selection_port):
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
        E       Orange   5           300
        B       Yellow   2           240
        F       Green    6           180
        A       Blue     1           120
        C       Purple   3           60

    """
    # check / test if it is better to get position with get_motor_encoder or by updating current position variable
    print("entered select")
    absolutePosition = BP.get_motor_encoder(selection_port)
    print("got encoding", absolutePosition)
    
    current_position = absolutePosition % 360

    mapping = {1: 120, 2: 240, 3: 60, 4: 0, 5: 300, 6: 180}
    
    desired_position = mapping[fire_type]
    print("f, d", fire_type, desired_position)
    # handle case where A is first
    # if (not done_before and (desired_position == 0)): 
    #     done_before = True
    #     print("exit")
    #     return 

    # relative move required
    relative_move = (desired_position - current_position) % 360
    if debug: 
        print ("Relative move: ", relative_move)

    # if relative move is greater than 180, move counterclockwise
    if relative_move > 180:
        relative_move -= 360
    # handle case where no move required 
    if relative_move == 0: 
        print ("goodbye")
        return

    # set motor to new relative position
    selection_motor.set_position_relative(relative_move)
    wait_for_motor(selection_motor)

    return
