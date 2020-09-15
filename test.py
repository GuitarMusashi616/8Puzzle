# Austin Williams, Jack Carroll
# Professor Moore
# Artificial Intelligence A405
# September 4 2020

# 1 2 3 8 0 4 7 6 5
# 2 8 1 0 4 3 7 6 5

# 1 2 3 8 0 4 7 6 5
# 3 7 2 1 6 0 8 5 4

# 7 2 4 5 0 6 8 3 1
# 0 1 2 3 4 5 6 7 8


from main import *


def test_misplaced():
    """used to test misplaced tiles heuristic"""
    initial_node = Node(State([[7, 2, 4],
                               [5, 0, 6],
                               [8, 3, 1]]))

    goal_node = Node(State([[0, 1, 2],
                            [3, 4, 5],
                            [6, 7, 8]]))

    print(misplaced_tiles(initial_node, goal_node))


def test_manhattan_distance():
    """used to test manhattan distance heuristic"""
    initial_node = Node(State([[7, 2, 4],
                               [5, 0, 6],
                               [8, 3, 1]]))

    goal_node = Node(State([[0, 1, 2],
                            [3, 4, 5],
                            [6, 7, 8]]))

    print(manhattan_distance(initial_node, goal_node))


def test_priority_node():
    """used to test priority queue functionality with priority nodes"""
    initial_node = PriorityNode(State([[1, 2, 3],
                                       [8, 0, 4],
                                       [7, 6, 5]]))

    goal_node = PriorityNode(State([[2, 8, 1],
                                    [0, 4, 3],
                                    [7, 6, 5]]))

    initial_node.set_priority(6)
    goal_node.set_priority(2)
    pq = PriorityQueue()
    pq.put(goal_node)
    pq.put(initial_node)
    while pq:
        print(pq.get())


def test_breadth_first():
    """used to test breadth first search"""
    initial_node = Node(State([[1, 2, 3],
                               [8, 0, 4],
                               [7, 6, 5]]))

    goal_node = Node(State([[2, 8, 1],
                            [0, 4, 3],
                            [7, 6, 5]]))

    found = breadth_first(initial_node, goal_node)
    instructions = [found]

    print("goal node")
    print(goal_node)
    while found.parent:
        instructions.append(found.parent)
        found = found.parent

    while instructions:
        node = instructions.pop()
        print(f"path cost: {node.path_cost}")
        print(node)


def test_greedy_best():
    """used to test greedy best search"""
    initial_pnode = PriorityNode(State([[1, 2, 3],
                                        [8, 0, 4],
                                        [7, 6, 5]]))

    goal_pnode = PriorityNode(State([[2, 8, 1],
                                     [0, 4, 3],
                                     [7, 6, 5]]))

    found = greedy_best(initial_pnode, goal_pnode)
    instructions = [found]

    while found.parent:
        instructions.append(found.parent)
        found = found.parent

    print("goal node")
    print(goal_pnode)
    while instructions:
        pnode = instructions.pop()
        print(f"path cost: {pnode.path_cost}")
        print(f"misplaced tiles: {pnode.priority}")
        print(pnode)


def test_a_star(heuristic=misplaced_tiles):
    """used to test A* with misplaced tiles and A* with manhattan distance"""
    initial_pnode = PriorityNode(State([[1, 2, 3],
                                        [8, 0, 4],
                                        [7, 6, 5]]))

    goal_pnode = PriorityNode(State([[2, 8, 1],
                                     [0, 4, 3],
                                     [7, 6, 5]]))

    found = a_star(initial_pnode, goal_pnode, heuristic)
    instructions = [found]

    while found.parent:
        instructions.append(found.parent)
        found = found.parent

    print("goal node")
    print(goal_pnode)
    while instructions:
        pnode = instructions.pop()
        print(f"path cost: {pnode.path_cost}")
        if pnode.priority:
            if heuristic == misplaced_tiles:
                print(f"misplaced tiles: {abs(pnode.priority - pnode.path_cost)}")
            else:
                print(f"manhattan distance: {abs(pnode.priority - pnode.path_cost)}")
            print(f"total priority: {pnode.priority}")

        print(pnode)