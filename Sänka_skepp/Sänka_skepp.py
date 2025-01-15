'''
Sänka_skepp.py: Sänka skepp spel med hjälp av matriser

__author__  = "Valter Carlens, Viktor Johansson Nygren"
__version__ = "1.0.0"
__email1__   = "Valter.Carlens@elev.ga.ntig.se"
__email2__   = "Viktor.Johansson.Nygren@elev.ga.ntig.se"
'''
import os
import random

def init():
    os.system("cls")
    print(f"Welcome to battleship game\nYou will be playing against a superpowerful AI\nYou will start by placing out your ships in the playingboard")

def build_playingboard(dims):
    return [["O" for count in range(dims)] for count in range(dims - 3)]

def print_playingboard(board):
    for i, b in enumerate(board):
        # Print each row with "O"s separated by spaces
        print(" | ".join(b))
        # Print separator line except after the last row
        if i < len(board) - 1:
            print("--+" + "---+" * (len(b) - 2) + "---")

def build_ship(dims):
    # Generate length of ship between number 1 - 5
    ship_len = random.randint(1, 5)
    ship_orientation = random.randint(0, 1)
    # Ship is horizontal if ship_orientation = 0 and vertical if ship_orienation = 1

    if ship_orientation == 0:
        # Randomly select row and create list of selected row * length of ship
        row_ship = [random.randint(0, dims - 1)] * ship_len


playingboard = build_playingboard(12)
print_playingboard(playingboard)

def main():
    pass