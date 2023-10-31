# Selection Subsystem Code
# Authors: Shidan Javaheri, Alice Godbout


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
        D - Red - 0 or 360
        E - Orange - 60
        B - Yellow - 120
        F - Green - 180
        A - Blue - 240
        C - Purple - 300

    """

    current_position = 0

    return color_position
