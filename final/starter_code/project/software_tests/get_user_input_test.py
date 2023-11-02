debug = True
city_state = [[0 for _ in range(4)] for _ in range(4)]
current_bearing = 0
current_position = (0, 0)
state = ""

print(city_state)


def get_user_input():
    """
    Gets the user input for the fire coordinates
    Convert coordinates into proper coordinates for array
    User will input (x,y). We will not adjust the values

    Format: x1,y1,LETTER1,x2,y2,LETTER,x3,y3,LETTER3

    Returns:
        list : a list of tuples representing the fire coordinates, in order of increasing distance from the starting position 0,0

    """

    fire_input = input(
        "Enter the fire coordinates (Format: x1,y1,LETTER1,x2,y2,LETTER,x3,y3,LETTER3): "
    )

    # split the input string at commas
    fire_list = []
    for i in range(0, len(fire_input.split(",")), 3):
        fire_list.append(fire_input.split(",")[i : i + 3])

    # convert letter (fire types) into integers
    fire_coords = []  # list containing only location
    fires = []  # list containing the location and types of fires
    for fire in fire_list:
        x = 3 - int(fire[1])
        y = int(fire[0])
        if debug:
            print("Fire Coordinates", x, y)
        fire_letters = ord(fire[2].upper()) - ord("A") + 1
        fire_coords.append((x, y))
        fires.append((x, y, fire_letters))

    # sort fires by increasing distance from (0,0)
    sorted_coords = sorted(fire_coords, key=lambda x: (x[0] ** 2 + x[1] ** 2) ** 0.5)

    # update city_map with fire types
    for x, y, fire_type in fires:
        city_state[x][y] = fire_type

    if debug:
        print("fire list", fire_list)
        print("fire coords", fire_coords)
        print("fire location and types", fires)
        print("sorted coords", sorted_coords)
        print("city_state", city_state)

    return sorted_coords


def display_loading_instructions():
    """
    Displays instructions for how to load the robot. Asks user to enter yes when loading is complete
    """
    # display instructions
    print(
        "Dear external robot operator, please follow the following instructions to load our robot. Do you confirm you want to continue?"
    )
    response = input()

    if "yes" in response.lower() or "y" in response.lower():
        print(
            "Place cubes according to the color represented on the cardboard placed on the wheel."
        )
        print("Once you've finished loading the robot, please confirm below.")

        # ask the user to enter 'yes' once loading is complete
        loading_response = ""
        while loading_response.lower() != "yes" and loading_response.lower() != "y":
            loading_response = input("Enter 'yes' or 'y' when loading is complete: ")
    else:
        print(
            "Loading instructions not displayed. Please confirm if you want to proceed."
        )

    print("Robot loading confirmed. Proceed to the next step.")
    return


coords = "2,2,A,1,1,B,2,3,F"
get_user_input()
