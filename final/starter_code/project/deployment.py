# Deployment Subsystem Code
# Authors: Shidan Javaheri, Alice Godbout
import time


# Main Function for Deployment Subsystem
# --------------------------------

def deploy_fire(deployment_motor): 
    """
    Deploys the fire suppressant 

    Args:
        deployment_motor (Motor): deployment motor

    Returns: 
        None
    """
    time.sleep(4)
    # deployment_motor.set_position_relative(360)
    return