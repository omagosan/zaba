import os

import numpy as np


class SudokuSolver:
    def __init__(self):
        self.field = np.zeros([9, 9], dtype=int)

    def load(self, file_path: str) -> None:

        # list of lists (rows)
        loaded_rows: list[list[int]] = []
        # implement loading of the file
        with open(file_path) as f:
            for line in f:
                row_numbers = []

                for value in line.split(";"):
                    row_numbers.append(int(value))

                loaded_rows.append(row_numbers)

        # convert nested list to numpy array
        self.field = np.array(loaded_rows)



    def check_sequence(self, sequence) -> bool:
        seen = set()

        for number in sequence:
            if number == 0:
                continue
            if number in seen:
                return False
            seen.add(number)

        return True


    def check_row(self, row_index: int) -> bool:
        return self.check_sequence(self.field[row_index])

    def check_column(self, column_index: int) -> bool:
        return self.check_sequence(self.field[...,column_index])

    def check_block(self, row_index: int, column_index: int) -> bool:
        block_start_row = row_index // 3 * 3
        block_start_column = column_index // 3 * 3

        block = self.field[block_start_row:block_start_row + 3, block_start_column:block_start_column + 3]
        block = block.flatten()

        return self.check_sequence(block)


    def check_one_cell(self, row_index: int , column_index: int) -> bool:
        return self.check_row(row_index) and self.check_column(column_index) and self.check_block(row_index, column_index)


    def get_empty_cell(self) -> tuple[int, int] | None:
        """ Gets the coordinates of the next empty field. """
        for r in range(9):
            for c in range(9):
                if self.field[r, c] == 0:
                    return r, c
        return None

    def solve(self) -> bool:
        """ Recursively solves the sudoku. """

        empty = self.get_empty_cell()

        if empty is None:
            return True

        r, c = empty

        for number in range(1, 10):
            self.field[r, c] = number

            if self.check_one_cell(r, c) and self.solve():
                return True


        self.field[r, c] = 0
        return False




def main() -> None:
    sudoku_solver = SudokuSolver()
    sudoku_solver.load("07-backtracking/sudoku.csv")
    print(sudoku_solver.solve())
    print(sudoku_solver.field)

if __name__ == "__main__":
    main()
