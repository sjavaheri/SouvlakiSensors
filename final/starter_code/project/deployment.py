# Deployment Subsystem Code
# Authors: Shidan Javaheri, Alice Godbout
import time
import brickpi3

# Main Function for Deployment Subsystem
# --------------------------------
SAMPLING_RATE=0.2

BP = brickpi3.BrickPi3()

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


def deploy_fire(deployment_motor): 
    """
    Deploys the fire suppressant 

    Args:
        deployment_motor (Motor): deployment motor

    Returns: 
        None
    """
    deployment_motor.set_position_relative(360)
    wait_for_motor(deployment_motor)
    return