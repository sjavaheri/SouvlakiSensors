# Tests for the Software Subsystem
# Authors: Shidan Javaheri, Alice Godbout

# import statements
from movement_subsystem import *
from selection_subsystem import *
from deployment_subsystem import *


# Test Shortest Path Algorithm
def test_shortest_path(): 
    test_graph = [
        [0, 0, 0, 0],
        [0, 0, 1, 2],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ]

    start_x, start_y = 0,0
    target_x, target_y = 1, 3

    path = shortest_path(test_graph, start_x, start_y, target_x, target_y)

    if path is not None:
        print("Shortest path:", path)
        return True
    else:
        print("No path found.")
        return False

print(test_shortest_path())
