# board.py

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [["O" for _ in range(cols)] for _ in range(rows)]

    def update(self, row, col, result):
        self.grid[row][col] = "X" if result == "hit" else "-"

    def get_cell(self, row, col):
        return self.grid[row][col]

    def reset(self):
        self.grid = [["O" for _ in range(self.cols)] for _ in range(self.rows)]
