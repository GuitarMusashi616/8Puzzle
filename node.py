# Austin Williams, Jack Carroll
# Professor Moore
# Artificial Intelligence A405
# September 4 2020


class Node:
    """Used to keep track of parents and path_cost, wrapper for state"""
    def __init__(self, state, parent=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost

    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return str(self.state)

    def expand(self):
        """
        swaps the 0 in the 8puzzle above, below, left, and right.
        creates a copy of each resulting action
        returns as a list of nodes
        """
        children = []
        if self.state.above(0):
            new_state = self.state.swap_up(0)
            new_node = Node(new_state, self, self.path_cost + 1)
            children.append(new_node)

        if self.state.below(0):
            new_state = self.state.swap_down(0)
            new_node = Node(new_state, self, self.path_cost + 1)
            children.append(new_node)

        if self.state.left_of(0):
            new_state = self.state.swap_left(0)
            new_node = Node(new_state, self, self.path_cost + 1)
            children.append(new_node)

        if self.state.right_of(0):
            new_state = self.state.swap_right(0)
            new_node = Node(new_state, self, self.path_cost + 1)
            children.append(new_node)

        return children


class PriorityNode(Node):
    """Priority Node used for sorting within a priority queue"""
    def __init__(self, state, parent=None, path_cost=0):
        super(PriorityNode, self).__init__(state, parent, path_cost)
        self.priority = None

    def set_priority(self, p):
        """
        used in priority queue
        """
        self.priority = p

    def __lt__(self, other):
        """
        used in priority queue
        """
        return self.priority < other.priority

    def expand(self):
        """
        Overridden to return PriorityNodes
        """
        children = []
        if self.state.above(0):
            new_state = self.state.swap_up(0)
            new_node = PriorityNode(new_state, self, self.path_cost + 1)
            children.append(new_node)

        if self.state.below(0):
            new_state = self.state.swap_down(0)
            new_node = PriorityNode(new_state, self, self.path_cost + 1)
            children.append(new_node)

        if self.state.left_of(0):
            new_state = self.state.swap_left(0)
            new_node = PriorityNode(new_state, self, self.path_cost + 1)
            children.append(new_node)

        if self.state.right_of(0):
            new_state = self.state.swap_right(0)
            new_node = PriorityNode(new_state, self, self.path_cost + 1)
            children.append(new_node)

        return children