import curses

def test_input(main_window):
    
    curses.curs_set(2)
    main_window.clear()
    main_window.addstr(0, 0, "Type something: ")
    main_window.clrtoeol()  # Clear line for input
    main_window.refresh()    # Refresh to show the updated window

    # Enable echoing of characters typed by the user
    curses.echo()

    # Get user input
    input_text = main_window.getstr(0, 16).decode("utf-8")  

    # Disable echoing again
    curses.noecho()

    # Display the input
    main_window.addstr(2, 0, f"You typed: {input_text}")  
    main_window.refresh()
    main_window.addstr(4, 0, "Press any key to exit.")
    main_window.refresh()
    main_window.getch()  # Wait for user to acknowledge

def main(stdscr):
    curses.curs_set(1)  # Show the cursor for input
    test_input(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)