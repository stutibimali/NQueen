# main.py
import tkinter as tk
from ui import NQueensGame

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGame(root)
    root.mainloop()
