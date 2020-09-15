# Austin Williams, Jack Carroll
# Professor Moore
# Artificial Intelligence A405
# September 4 2020

from queue import PriorityQueue


def parity_check(start, end):
    """
    Checks the boards' parity to ensure a solution is possible
    :param start: 2D int arr
    :param end: 2D int arr
    :return: bool
    """
    # Converts 2D to 1D array
    fresh_start = []
    dead_end = []
    for i in range(0, 3):
        for j in range(0, 3):
            fresh_start.append(start[i][j])
            dead_end.append(end[i][j])
    fresh_start.remove(0)
    dead_end.remove(0)

    # Calculate start and end array parity
    start_parity = 0
    end_parity = 0
    for i in range(0, 7):
        for j in range(i + 1, 8):
            if fresh_start[i] < fresh_start[j]:
                start_parity = start_parity + 1
            if dead_end[i] < dead_end[j]:
                end_parity = end_parity + 1

    if start_parity % 2 == end_parity % 2:
        return True
    else:
        return False


def misplaced_tiles(resulting_node, solution):
    """
    returns how many of the 8 numbered tiles in the resulting_node are misplaced with respect to the solution node
    """
    """
    :type resulting_node: Node
    :type solution: Node
    :rtype: int
    """
    initial_grid = resulting_node.state.grid
    goal_grid = solution.state.grid

    # error check
    assert len(initial_grid) == 3
    assert len(goal_grid) == 3

    # iterate over list of list
    num_misplaced = 0
    for r in range(3):
        assert len(initial_grid[r]) == 3
        assert len(goal_grid[r]) == 3
        for c in range(3):
            if initial_grid[r][c] != 0 and initial_grid[r][c] != goal_grid[r][c]:
                num_misplaced += 1

    return num_misplaced


def manhattan_distance(resulting_node, solution):
    """
    for each numbered tile in the resulting node, calculates how many blocks away the tile is from where it is
    supposed to be when solved, returns the sum
    """
    """
   :type resulting_node: Node
   :type solution: Node
   :rtype: int
   """
    initial_state = resulting_node.state
    goal_state = solution.state
    distance = 0

    for i in range(1, 9):
        r1, c1 = initial_state.find(i)
        r2, c2 = goal_state.find(i)
        distance += abs(r1 - r2) + abs(c1 - c2)

    return distance


def breadth_first(problem, solution):
    """
    branches problem node breadth first until a matching node is found, returns the matching node
    """
    """
    :type problem: Node
    :type solution: Node
    :rtype: Node
    """
    frontier = [problem]
    ignore = []
    add(ignore, problem)

    expanded_nodes = 0
    unexpanded_nodes = 1

    while frontier:
        leaf_node = frontier.pop(0)

        if leaf_node == solution:
            print(f"expanded nodes: {expanded_nodes}")
            print(f"unexpanded nodes: {unexpanded_nodes}\n")
            return leaf_node

        unexpanded_nodes -= 1
        expanded_nodes += 1
        # print(expanded_nodes)
        # print(unexpanded_nodes)
        # print(len(ignore))

        for resulting_node in leaf_node.expand():
            # Uses binary search on sorted array ignore to see if node is already in frontier or has already been expanded
            if search(ignore, resulting_node):
                pass
            else:
                frontier.append(resulting_node)
                # Adds and sorts the resulting node to the ignore array so we know not to add it to frontier again
                ignore = add(ignore, resulting_node)
                unexpanded_nodes += 1


def add(ignore, resulting_node):
    temp_arr = []
    for i in range(0, 3):
        for j in range(0, 3):
            temp_arr.append(resulting_node.state.grid[i][j])
    res = int("".join(map(str, temp_arr)))
    temp_int = int(res)
    if len(ignore) == 0:
        ignore.append(temp_int)
    else:
        for i in range(len(ignore)):
            if ignore[i] > temp_int:
                index = i
                break
        ignore = ignore[:i] + [temp_int] + ignore[i:]
        return ignore


def search(ignore, resulting_node):
    temp_arr = []
    for i in range(0, 3):
        for j in range(0, 3):
            temp_arr.append(resulting_node.state.grid[i][j])
    res = int("".join(map(str, temp_arr)))
    temp_int = int(res)
    present = binary_search(ignore, 0, len(ignore) - 1, temp_int)
    return present


def binary_search(arr, l, r, x):
    # Check base case
    if r >= l:

        mid = l + (r - l) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return True

            # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, l, mid - 1, x)

            # Else the element can only be present
        # in right subarray
        else:
            return binary_search(arr, mid + 1, r, x)

    else:
        # Element is not present in the array
        return False


def greedy_best(problem, solution):
    """
    expands problem node and appends to priority queue, nodes with lowest misplaced tiles are tested first,
    returns node that matches solution
    """
    """
    :type problem: PriorityNode
    :type solution: PriorityNode
    :rtype: PriorityNode
    """
    frontier = PriorityQueue()
    frontier.put(problem)
    explored = []

    expanded_nodes = 0
    unexpanded_nodes = 1

    while frontier:
        leaf_node = frontier.get()

        if leaf_node == solution:
            print(f"expanded nodes: {expanded_nodes}")
            print(f"unexpanded nodes: {unexpanded_nodes}\n")
            return leaf_node

        explored.append(leaf_node)
        unexpanded_nodes -= 1
        expanded_nodes += 1

        for resulting_node in leaf_node.expand():
            if resulting_node in frontier.queue or resulting_node in explored:
                pass
            else:
                priority = misplaced_tiles(resulting_node, solution)
                resulting_node.set_priority(priority)
                frontier.put(resulting_node)
                unexpanded_nodes += 1


def a_star(problem, solution, heuristic=misplaced_tiles):
    """
    expands problem node and appends to priority queue,
    priority is determined by (misplaced_tiles or manhattan_distance) + path_cost
    returns node that matches solution
    """
    """
   :type problem: PriorityNode
   :type solution: PriorityNode
   :type heuristic: function
   :rtype: PriorityNode
   """
    frontier = PriorityQueue()
    frontier.put(problem)
    explored = []

    expanded_nodes = 0
    unexpanded_nodes = 1

    while frontier:
        leaf_node = frontier.get()

        if leaf_node == solution:
            print(f"expanded nodes: {expanded_nodes}")
            print(f"unexpanded nodes: {unexpanded_nodes}\n")
            return leaf_node

        explored.append(leaf_node)
        expanded_nodes += 1
        unexpanded_nodes -= 1

        for resulting_node in leaf_node.expand():
            if resulting_node in frontier.queue or resulting_node in explored:
                pass
            else:
                priority = heuristic(resulting_node, solution)
                resulting_node.set_priority(priority + resulting_node.path_cost)
                frontier.put(resulting_node)
                unexpanded_nodes += 1
