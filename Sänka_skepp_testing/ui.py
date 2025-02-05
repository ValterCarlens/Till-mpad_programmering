# ui.py
import tkinter as tk
from tkinter import messagebox

class BattleshipUI:
    def __init__(self, game):
        self.game = game
        self.game.total_guesses = 0  # Initialize guess counter
        self.root = tk.Tk()
        self.root.title("Battleship Game")
        self.buttons = []
        self.show_welcome_screen()

    def show_welcome_screen(self):
        welcome_frame = tk.Frame(self.root)
        welcome_frame.pack(expand=True)

        tk.Label(welcome_frame, text="Welcome to Battleship!", font=("Arial", 16), pady=20).pack()
        tk.Button(welcome_frame, text="Start Game", command=lambda: self.start_game(welcome_frame), width=15).pack(pady=10)
        tk.Button(welcome_frame, text="Quit", command=self.root.quit, width=15).pack(pady=5)

    def start_game(self, welcome_frame):
        welcome_frame.destroy()
        if hasattr(self.game, 'board') and self.game.board:
            self.create_board()
        else:
            messagebox.showerror("Error", "Game board not initialized correctly.")

    def create_board(self):
        for row in range(self.game.board.rows):
            button_row = []
            for col in range(self.game.board.cols):
                button = self.create_button(row, col)
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def create_button(self, row, col):
        return tk.Button(self.root, text="O", width=4, height=2,
                          command=lambda r=row, c=col: self.handle_guess(r, c))

    def handle_guess(self, row, col):
        self.game.total_guesses += 1  # Increment guess counter
        result = self.game.make_guess(row, col)

        if result == "already_guessed":
            messagebox.showinfo("Info", "You already guessed that spot!")
        elif result == "hit":
            self.buttons[row][col].config(text="X", bg="red")
        elif result == "miss":
            self.buttons[row][col].config(text="-", bg="blue")
        elif result == "sunk":
            self.buttons[row][col].config(text="X", bg="green")
            messagebox.showinfo("Congratulations!", "You've sunk a ship!")
        elif result == "game_won":
            self.buttons[row][col].config(text="X", bg="green")
            self.show_results_popup("Victory!", "Congratulations! You've sunk all the ships!")
        elif result == "game_over":
            self.buttons[row][col].config(text="-", bg="blue")
            self.show_results_popup("Game Over", "You've used all your guesses. Game Over!")

    def get_guess_count(self):
        return self.game.total_guesses

    def show_results_popup(self, title, message):
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("300x200")
        result_window.grab_set()  # Disable main window interaction

        guesses_made = self.get_guess_count()
        stats_message = f"{message}\n\nTotal Guesses: {guesses_made}"

        tk.Label(result_window, text=stats_message, font=("Arial", 12), pady=20).pack()
        tk.Button(result_window, text="OK", command=self.root.quit).pack(pady=10)

    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.cleanup()

    def cleanup(self):
        self.root.destroy()