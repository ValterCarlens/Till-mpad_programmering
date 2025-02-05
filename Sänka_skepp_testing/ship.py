# ship.py
import random

class Ship:
    def __init__(self, rows, cols, occupied_positions):
        self.length = random.randint(1, 7)
        self.orientation = random.choice(["horizontal", "vertical"])
        self.coordinates = []

        # Place ship ensuring no overlap and one-cell gap
        while True:
            if self.orientation == "horizontal":
                row = random.randint(0, rows - 1)
                col_start = random.randint(0, cols - self.length)
                potential_coords = [(row, col) for col in range(col_start, col_start + self.length)]
            else:
                col = random.randint(0, cols - 1)
                row_start = random.randint(0, rows - self.length)
                potential_coords = [(row, col) for row in range(row_start, row_start + self.length)]

            if self.is_valid_placement(potential_coords, occupied_positions, rows, cols):
                self.coordinates = potential_coords
                occupied_positions.update(self.get_buffer_zone())
                break

    def is_valid_placement(self, coords, occupied_positions, rows, cols):
        for coord in coords:
            if coord in occupied_positions:
                return False

        # Check buffer zone
        for coord in coords:
            row, col = coord
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < rows and 0 <= c < cols and (r, c) in occupied_positions:
                        return False
        return True

    def get_buffer_zone(self):
        buffer_zone = set()
        for row, col in self.coordinates:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    buffer_zone.add((r, c))
        return buffer_zone

    def hit(self, coord):
        if coord in self.coordinates:
            self.coordinates.remove(coord)
            return True
        return False

    def is_sunk(self):
        return len(self.coordinates) == 0