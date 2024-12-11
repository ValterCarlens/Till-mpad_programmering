import curses
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.addstr("hej")

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)