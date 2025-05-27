import tkinter as tk
from ui_main import BudgetManagerApp

'''
main.py: denna fil innehåller programmets huvudloop och huvudfönster

__author__  = "Valter Carlens"
__version__ = "1.0.0"
__email__   = "valter.carlens@elev.ga.ntig.se"
'''

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetManagerApp(root)
    root.mainloop() 
