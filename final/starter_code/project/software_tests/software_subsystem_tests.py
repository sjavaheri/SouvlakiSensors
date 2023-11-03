# Tests for the Software Subsystem
# Authors: Shidan Javaheri, Alice Godbout

# import statements
from movement import *

# Test Graphs 
# ----------------

test_graph1 = [
        [0, 0, 0, 0],
        [0, 0, 1, 2],
        [0, 0, 0, 3],
        [0, 0, 0, 0]
    ]

test_graph2 = [
        [0, 0, 0, 0],
        [4, 0, 0, 0],
        [0, 0, 0, 2],
        [0, 1, 0, 0]
    ]


def check_results1(start_x, start_y, target_x, target_y, test_graph=test_graph1):
    """
    checks the path between start and end points on test graph 1

    Args: 
        start_x (int): x coordinate of start point
        start_y (int): y coordinate of start point
        target_x (int): x coordinate of end point
        target_y (int): y coordinate of end point

    Returns: 
        bool: True if path exists, False otherwise
    """

    path = shortest_path(test_graph, start_x, start_y, target_x, target_y)

    if path is not None:
        print("Shortest path:", path)
        return True
    else:
        print("No path found.")
        return False


# Test Shortest Path Algorithm
def test_shortest_path1(): 
    """
    Test for graph 1
    """

    start_x, start_y = 3,0
    target_x, target_y = 1, 3

    print("Results from Test 1: " + str(check_results1(start_x, start_y, target_x, target_y)))

    start_x, start_y = 0,3
    target_x, target_y = 1, 3

    print("Results from Test 2: " + str(check_results1(start_x, start_y, target_x, target_y)))

    start_x, start_y = 0,3
    target_x, target_y = 2, 3

    print("Results from Test 3: " + str(check_results1(start_x, start_y, target_x, target_y)))

def test_shortest_path2():
    """
    Test for graph 2
    """
    start_x, start_y = 0,0
    target_x, target_y = 1, 0

    print("Results from Test 1: " + str(check_results1(start_x, start_y, target_x, target_y, test_graph=test_graph2)))

    start_x, start_y = 0,0
    target_x, target_y = 2,3

    print("Results from Test 2: " + str(check_results1(start_x, start_y, target_x, target_y , test_graph=test_graph2)))

    start_x, start_y = 1,3 
    target_x, target_y = 3,1

    print("Results from Test 3: " + str(check_results1(start_x, start_y, target_x, target_y, test_graph=test_graph2)))

# Run Tests
test_shortest_path1()
test_shortest_path2()  

