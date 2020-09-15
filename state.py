# Austin Williams, Jack Carroll
# Professor Moore
# Artificial Intelligence A405
# September 4 2020


class State:
    """used to easily mutate the state representation"""
    def __init__(self, grid, rows=3, columns=3):
        self.grid = grid
        self.rows = rows
        self.columns = columns

    def __str__(self):
        """visual representation of the sliding puzzle"""
        s = ""
        for row in self.grid:
            s += str(row)
            s += '\n'
        return s

    def __eq__(self, other):
        return self.grid == other.grid

    def above(self, n):
        """returns number above n or false"""
        r, c = self.find(n)
        if r == 0:
            return False
        return self.grid[r - 1][c]

    def below(self, n):
        """returns number below n or false"""
        r, c = self.find(n)
        if r == self.rows - 1:
            return False
        return self.grid[r + 1][c]

    def left_of(self, n):
        """returns number left of n or false"""
        r, c = self.find(n)
        if c == 0:
            return False
        return self.grid[r][c - 1]

    def right_of(self, n):
        """returns number right of n or false"""
        r, c = self.find(n)
        if c == self.columns - 1:
            return False
        return self.grid[r][c + 1]

    def swap_up(self, n):
        """swaps n with number above n"""
        r, c = self.find(n)
        if r == 0:
            raise KeyError("No tile above " + str(n))

        new_state = []
        for row in self.grid:
            new_state.append(row.copy())
        new_state[r][c] = self.grid[r - 1][c]
        new_state[r - 1][c] = n

        return State(new_state)

    def swap_down(self, n):
        """swaps n with number below n"""
        r, c = self.find(n)
        if r == self.rows - 1:
            raise KeyError("No tile below " + str(n))

        new_state = []
        for row in self.grid:
            new_state.append(row.copy())
        new_state[r][c] = self.grid[r + 1][c]
        new_state[r + 1][c] = n

        return State(new_state)

    def swap_left(self, n):
        """swaps n with number left of n"""
        r, c = self.find(n)
        if c == 0:
            raise KeyError("No tile to the left " + str(n))

        new_state = []
        for row in self.grid:
            new_state.append(row.copy())
        new_state[r][c] = self.grid[r][c - 1]
        new_state[r][c - 1] = n

        return State(new_state)

    def swap_right(self, n):
        """swaps n with number right of n"""
        r, c = self.find(n)
        if c == self.columns - 1:
            raise KeyError("No tile to the right " + str(n))

        new_state = []
        for row in self.grid:
            new_state.append(row.copy())
        new_state[r][c] = self.grid[r][c + 1]
        new_state[r][c + 1] = n

        return State(new_state)

    def find(self, n):
        """returns integers: row, column of n"""
        for i, row in enumerate(self.grid):
            if n in row:
                return i, row.index(n)