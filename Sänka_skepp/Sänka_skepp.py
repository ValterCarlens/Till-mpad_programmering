import os
import random
from tkinter import *

def init():
    os.system("cls" if os.name == "nt" else "clear")
    print("Welcome to Battleship!\nYou will be playing against a super-powerful AI.\n"
          "You will start by placing your ships on the playing board.\n")


def build_playingboard(rows, cols):
    return [["O" for _ in range(cols)] for _ in range(rows)]


def print_playingboard(board):
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < len(board) - 1:
            print("--+" + "---+" * (len(row) - 2) + "---")


def build_ship(rows, cols):
    ship_len = random.randint(1, 7)  # Ship length between 1 and 7
    ship_orientation = random.choice(["horizontal", "vertical"])
    coords = []

    if ship_orientation == "horizontal":
        row = random.randint(0, rows - 1)
        col_start = random.randint(0, cols - ship_len)
        coords = [(row, col) for col in range(col_start, col_start + ship_len)]
    else:
        col = random.randint(0, cols - 1)
        row_start = random.randint(0, rows - ship_len)
        coords = [(row, col) for row in range(row_start, row_start + ship_len)]

    return coords


def update_playingboard(guess, playingboard, ship, guesses):
    if guess in guesses:
        print("You already guessed that spot!")
        return playingboard

    guesses.append(guess)
    if guess in ship:
        print("You hit a ship!")
        playingboard[guess[0]][guess[1]] = "X"
        ship.remove(guess)
    else:
        print("Miss!")
        playingboard[guess[0]][guess[1]] = "-"

    return playingboard


def user_guess(rows, cols):
    while True:
        try:
            row = int(input(f"Enter row (1-{rows}): ")) - 1
            col = int(input(f"Enter column (1-{cols}): ")) - 1

            if 0 <= row < rows and 0 <= col < cols:
                return row, col
            else:
                print(f"Please enter numbers between 1 and {rows} for rows, and 1 and {cols} for columns.")
        except ValueError:
            print("Invalid input. Please enter numbers only.")


def main():
    rows, cols = 9, 12  # Dimensions of the board
    board = build_playingboard(rows, cols)
    ship = build_ship(rows, cols)
    guesses = []

    print("Here is the board:")
    print_playingboard(board)

    while len(ship) > 0:
        print("\nTake your guess!")
        guess = user_guess(rows, cols)
        board = update_playingboard(guess, board, ship, guesses)
        print_playingboard(board)

    print("Congratulations! You've sunk all the ships!")


if __name__ == "__main__":
    init()
    main()
