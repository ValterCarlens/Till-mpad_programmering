'''
main.py: denna fil hanterar användarens gissningar, kontrollerar om alla skepp blivit sänkta samt resetar brädet när spelet är klart 

__author__  = "Valter Carlens, Viktor Johansson Nygren"
__version__ = "1.0.0"
__email__   = "valter.carlens@elev.ga.ntig.se, viktor.johannsonnygren@elev.ga.ntig.se"
'''

from board import Board
from ship import Ship

class BattleshipGame:
    def __init__(self, rows, cols, num_ships=5):
        self.board = Board(rows, cols)
        self.occupied_positions = set()
        self.ships = [Ship(rows, cols, self.occupied_positions) for _ in range(num_ships)]
        self.guesses = []
        self.max_guesses = rows * cols

    def make_guess(self, row, col):
        if (row, col) in self.guesses:
            return "already_guessed"

        self.guesses.append((row, col))
        for ship in self.ships:
            if ship.hit((row, col)):
                self.board.update(row, col, "hit")
                if ship.is_sunk():
                    if self.all_ships_sunk():
                        return "game_won"
                    return "sunk"
                return "hit"

        self.board.update(row, col, "miss")
        if len(self.guesses) == self.max_guesses:
            return "game_over"
        return "miss"

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def reset_game(self):
        self.board.reset()
        self.occupied_positions = set()
        self.ships = [Ship(self.board.rows, self.board.cols, self.occupied_positions) for _ in range(5)]
        self.guesses = []
