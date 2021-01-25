from colorama import Fore, Style
import itertools
from more_itertools import grouper

test = [
    '5', '3', ' ', ' ', '7', ' ', ' ', ' ', ' ',
    '6', ' ', ' ', '1', '9', '5', ' ', ' ', ' ',
    ' ', '9', '8', ' ', ' ', ' ', ' ', '6', ' ',
    '8', ' ', ' ', ' ', '6', ' ', ' ', ' ', '3',
    '4', ' ', ' ', '8', ' ', '3', ' ', ' ', '1',
    '7', ' ', ' ', ' ', '2', ' ', ' ', ' ', '6',
    ' ', '6', ' ', ' ', ' ', ' ', '2', '8', ' ',
    ' ', ' ', ' ', '4', '1', '9', ' ', ' ', '5',
    ' ', ' ', ' ', ' ', '8', ' ', ' ', '7', '9'
    ]

class Board:
    """Create Sudoku board represented by 81 values."""
    def __init__(self, values):
        self.values = values
        self.initial_indices = [index for index, entry in enumerate(values) if entry != " "]

    @property
    def rows(self):
        return grouper(self.values, 9)

    @property
    def columns(self):
        return zip(*grouper(self.values, 9))

    @property
    def subgrids(self):
        """Create lists with values of each 3x3 subgrid."""
        subgrids = []
        for h, i in itertools.product(range(3), repeat=2):
            subgrid = iter(self.values[27*h + 3*i + 9*j + k] for j, k in itertools.product(range(3), repeat=2))
            subgrids.append(subgrid)
        return subgrids

    @property
    def solved(self):
        """Check if board is solved."""
        for section in itertools.chain(self.rows, self.columns, self.subgrids):
            if not is_solved_section(section):
                return False
        return True

    def print_board(self):
        """Print current state of board."""
        column_labels = map(str, range(1, 10))
        print("    " + "   ".join(column_labels))
        print("  " + Fore.CYAN + "-"*37 + Style.RESET_ALL)
        for i, row in enumerate(self.rows):
            row_str = f"{i+1} "
            for j, column in enumerate(row):
                index = 9*i + j
                if j%3 == 0:
                    row_str += Fore.CYAN
                else:
                    row_str += Style.RESET_ALL
                row_str += "| "
                if index in self.initial_indices:
                    row_str += Fore.YELLOW
                else:
                    row_str += Fore.GREEN
                row_str += column + " "
            row_str += Fore.CYAN + "|" + Style.RESET_ALL
            print(row_str)
            border_str = "  "
            if i%3 == 2:
                border_str += Fore.CYAN
            border_str += "-"*37 + Style.RESET_ALL
            print(border_str)

    def change_space(self, row, column, value):
        """Change value of space on board."""
        index = 9*(row - 1) + column - 1
        if index in self.initial_indices:
            return
        else:
            self.values[9*(row - 1) + column - 1] = str(int(value))

    def accept_input(self):
        """Get input from user and change board based on input."""
        user_values = input("Enter the row, column, and value separated by commas: ")
        [row, column, value] = [x.strip() for x in user_values.split(",")]
        self.change_space(int(row), int(column), value)
        self.print_board()

def remove_blank_entries(value_list):
    """Remove blank values from list."""
    return [x for x in value_list if x != " "]

def is_valid_section(section):
    """Check section of the board (row, column, or subgrid) for valid entries."""
    section = remove_blank_entries(section)
    # Check for duplicate values.
    if len(set(section)) != len(section):
        return False
    else:
        return True

def is_complete_section(section):
    """Check if board section (row, column, or subgrid) is completely filled out."""
    if " " not in section:
        return True
    else:
        return False

def is_solved_section(section):
    """Check if board section (row, column, or subgrid) is solved."""
    if is_valid_section(section) and is_complete_section(section):
        return True
    else:
        return False

board = Board(test)
board.print_board()

while(not board.solved):
    board.accept_input()
