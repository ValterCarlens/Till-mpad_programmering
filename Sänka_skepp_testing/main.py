# main.py
from game import BattleshipGame
from ui import BattleshipUI


def main():
    game = BattleshipGame(rows=9, cols=12)
    ui = BattleshipUI(game)
    ui.run()


if __name__ == "__main__":
    main()
