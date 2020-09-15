# Austin Williams, Jack Carroll
# Professor Moore
# Artificial Intelligence A405
# September 4 2020

from node import *
from searches import *
from state import *
from test import *


def get_start():
    """
    Gets starting board from user
    :return: A 2D int array
    """
    while True:
        usr_start = input("\nPlease input your start state as a line of numbers separated by spaces,"
                          # "\nStart with the top row and list numbers from left to right, repeat with descending rows:"
                          "\nex: 1 2 3 4 5 6 7 8 0\n")

        start_board = create_board(usr_start)
        if start_board:
            print("Your starting board:")
            print_board(start_board)
            return start_board
        else:
            print("Invalid input. Please try again.\n")


def get_end():
    """
    Gets desired end board state from user
    :return: 2D int array
    """
    while True:
        usr_end = input("\nPlease input your desired end state as a line of numbers separated by spaces: "
                        "\nex: 1 2 3 4 5 6 7 8 0\n")
        end_board = create_board(usr_end)
        if end_board:
            print("Your end state:")
            print_board(end_board)
            return end_board
        else:
            print("Invalid input. Please try again.\n")


def get_search():
    """
    Gets search protocol from user
    :return: int
    """
    while True:
        search_type = input("\nWhich search would you like to run?\n"
                            "0) Run all searches\n"
                            "1) Breadth-First\n"
                            "2) Greedy-Best\n"
                            "3) A* (Misplaced tiles heuristic)\n"
                            "4) A* (Manhattan distance heuristic)\n"
                            "-1) Exit\n")
        try:
            search_type = int(search_type)
        except ValueError:
            print("invalid response, please enter a number")

        if search_type in [-1, 0, 1, 2, 3, 4]:
            return search_type
        else:
            print("Sorry, that is an invalid response.\n")


def create_board(input):
    """
    Creates a game board given the user input
    if input is invalid, throws exception
    :param input:
    :return: A 2-dimensional int array
    """

    # Creates int array from user input
    str_arr = input.split()
    int_arr = []
    for x in str_arr:
        try:
            int_arr.append(int(x))
        except:
            return None
    # Checks input will make a valid board
    valid = test_valid(int_arr)
    # If valid, creates the board
    board = []
    if valid:
        row_1, row_2, row_3 = [], [], []
        for i in range(0, 3):
            row_1.append(int_arr[i])
            row_2.append(int_arr[i + 3])
            row_3.append(int_arr[i + 6])
        board.append(row_1)
        board.append(row_2)
        board.append(row_3)
        return board
    else:
        return None


def print_board(board):
    for row in board:
        print(row)


def run_search(start_board, end_board, search_type):
    """
    Takes in an integer to determine which search to run
    Runs desired search/searches
    :param search_type: int
    :param start_board: 2D int arr
    :param end_board: 2D int arr
    :return: bool
    """
    # Runs parity check to ensure the board is possible
    possible = parity_check(start_board, end_board)
    if possible:
        print("\nBoards pass parity check.\n")
    else:
        print("\nBoards do not pass parity check. Solution impossible.\n")
        return
    # Determines which search to run
    if search_type == 1:
        print("Breadth-First Search Results:\n")
        run_breadth(start_board, end_board)

    elif search_type == 2:
        print("\nGreedy Best-First Search Results:\n")
        run_greedy(start_board, end_board)

    elif search_type == 3:
        print("\nA* Search With Misplaced Tiles Heuristic Results:\n")
        run_a_star(misplaced_tiles, start_board, end_board)

    elif search_type == 4:
        print("\nA* Search With Manhattan Distance Heuristic Results:\n")
        run_a_star(manhattan_distance, start_board, end_board)

    elif search_type == 0:
        print("Breadth-First Search Results:\n")
        run_breadth(start_board, end_board)
        print("\nGreedy Best-First Search Results:\n")
        run_greedy(start_board, end_board)
        print("\nA* Search With Misplaced Tiles Heuristic Results:\n")
        run_a_star(misplaced_tiles, start_board, end_board)
        print("\nA* Search With Manhattan Distance Heuristic Results:\n")
        run_a_star(manhattan_distance, start_board, end_board)


def test_valid(int_arr):
    """
    Takes in an integer array and determines if
    it is valid to make a board
    :param int_arr: integer array
    :return: bool
    """

    # Checks correct number of numbers
    if len(int_arr) != 9:
        return False
    # Creates array with necessary values and compares to intArr
    compare = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    if set(compare).issubset(int_arr) and set(int_arr).issubset(compare):
        return True
    else:
        return False


def run_breadth(start_board, end_board):
    """
    Runs breadth first search
    :param start_board: 2D int arr
    :param end_board: 2D int arr
    """
    # Converts arr to node
    start_board = Node(State(start_board))
    end_board = Node(State(end_board))

    found = breadth_first(start_board, end_board)
    instructions = [found]

    while found.parent:
        instructions.append(found.parent)
        found = found.parent

    while instructions:
        node = instructions.pop()
        print(f"path cost: {node.path_cost}")
        print(node)


def run_greedy(start_board, end_board):
    """
    Runs Greedy best-first search
    :param start_board: 2D int arr
    :param end_board: 2D int arr
    """
    # Converts arr to node
    start_board = PriorityNode(State(start_board))
    end_board = PriorityNode(State(end_board))

    found = greedy_best(start_board, end_board)
    instructions = [found]

    while found.parent:
        instructions.append(found.parent)
        found = found.parent

    while instructions:
        pnode = instructions.pop()
        print(f"path cost: {pnode.path_cost}")
        print(f"misplaced tiles: {pnode.priority}")
        print(pnode)


def run_a_star(heuristic, start_board, end_board):
    """
    Runs A* Search
    :param heuristic: method
    :param start_board: 2D int arr
    :param end_board: 2D int arr
    """
    # Converts arr to node
    start_board = PriorityNode(State(start_board))
    end_board = PriorityNode(State(end_board))

    found = a_star(start_board, end_board, heuristic)
    instructions = [found]

    while found.parent:
        instructions.append(found.parent)
        found = found.parent

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


def main():
    """
    Main executable block. Gets user input, requests search type,
    runs desired search and prints solution.
    To run built in tests: test_breadth_first(), test_greedy_best(),
    test_a_star() (Runs with Misplaced Tiles heuristic by default),
    test_a_start(manhattan_distance) (Runs with Manhattan distance heuristic)
    """
    # Gets valid starting board from user
    start_board = get_start()

    # Gets valid end board from user
    end_board = get_end()

    # Gets desired search from user
    search_type = get_search()
    while search_type != -1:
        # Runs searches
        run_search(start_board, end_board, search_type)
        search_type = get_search()


if __name__ == '__main__':
    main()
