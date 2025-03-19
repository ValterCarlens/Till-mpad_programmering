# main.py
from game import BattleshipGame
from battleship_ui import BattleshipUI


def main():
    game = BattleshipGame(rows=9, cols=12) # Initiera bredd och höjd på brädet
    ui = BattleshipUI(game)
    ui.run()


if __name__ == "__main__":
    main() # Kör programmet
