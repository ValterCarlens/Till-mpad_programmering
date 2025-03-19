# ship.py
import random

class Ship:
    # Initiera skäpp-egenskaper
    def __init__(self, rows, cols, occupied_positions):
        self.length = random.randint(1, 7) # Gör skepp random-längd från 1 - 7 cell(s)
        self.orientation = random.choice(["horizontal", "vertical"]) # Slumpa skepp-riknting mellan vertikalt och horisontalt
        self.coordinates = [] # Initiera koordinater

        # Försäkra att det är en cell mellan de olika skeppen, samt mellan skeppen och sidan på planen
        while True:
            if self.orientation == "horizontal":
                row = random.randint(0, rows - 1) # Tilldela skeppet en "row"
                col_start = random.randint(0, cols - self.length)
                potential_coords = [(row, col) for col in range(col_start, col_start + self.length)]
            else:
                # Om skeppet är orienterat vertikalt
                col = random.randint(0, cols - 1)
                row_start = random.randint(0, rows - self.length)
                potential_coords = [(row, col) for row in range(row_start, row_start + self.length)]

            # Kolla koordinaterna för att se till att skeppen inte överlappar varandra
            if self.is_valid_placement(potential_coords, occupied_positions, rows, cols):
                self.coordinates = potential_coords
                occupied_positions.update(self.get_buffer_zone()) # Sparar koordinaterna om skeppen inte överlappar
                break

    # Checkar om skeppen överlappar, returnerar False om överlapp sker
    def is_valid_placement(self, coords, occupied_positions, rows, cols):
        for coord in coords:
            if coord in occupied_positions:
                return False

        # Kollar bufferzon mellan skepp, om returnerar true är placeringen valid
        for coord in coords:
            row, col = coord
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < rows and 0 <= c < cols and (r, c) in occupied_positions:
                        return False
        return True

    # Beräknar och returnerar en buffertzon runt skeppet
    def get_buffer_zone(self):
        buffer_zone = set()
        for row, col in self.coordinates: # Två nästlade loopar som beräknar en buffertzon med en cell runt skeppet
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    buffer_zone.add((r, c))
        return buffer_zone

    # Checkar träff
    def hit(self, coord):
        if coord in self.coordinates:
            self.coordinates.remove(coord)
            return True
        return False

    # Checkar miss
    def is_sunk(self):
        return len(self.coordinates) == 0