'''
main.py: main-programmet där spelet startas

__author__  = "Valter Carlens, Viktor Johansson Nygren"
__version__ = "1.0.0"
__email__   = "valter.carlens@elev.ga.ntig.se, viktor.johannsonnygren@elev.ga.ntig.se"
'''

from game import BattleshipGame
from battleship_ui import BattleshipUI


def main():
    game = BattleshipGame(rows=9, cols=12) # Initiera bredd och höjd på brädet
    ui = BattleshipUI(game)
    ui.run()


if __name__ == "__main__":
    main() # Kör programmet
