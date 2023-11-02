# Deployment Subsystem Code
# Authors: Shidan Javaheri, Alice Godbout



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
    deployment_motor.set_position_relative(360)
    return