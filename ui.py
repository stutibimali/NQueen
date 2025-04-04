import tkinter as tk
from tkinter import ttk
import subprocess
import sys

class NQueensUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Game")
        
        self.previous_scores = []
        
        self.load_previous_scores()
        self.create_welcome_screen()

    def create_welcome_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        welcome_frame = ttk.Frame(self.root, padding="10")
        welcome_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(welcome_frame, text="Welcome to N-Queens Challenge!", font=("Arial", 14)).grid(row=0, column=0, pady=10)
        ttk.Button(welcome_frame, text="Start Today's Challenge", command=self.start_todays_challenge).grid(row=1, column=0, pady=10)
        ttk.Button(welcome_frame, text="Scoreboard", command=self.show_scoreboard).grid(row=2, column=0, pady=10)
    
    def show_scoreboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        scoreboard_frame = ttk.Frame(self.root, padding="10")
        scoreboard_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(scoreboard_frame, text="Scoreboard", font=("Arial", 14)).grid(row=0, column=0, pady=10)
        for i, score in enumerate(self.previous_scores):
            ttk.Label(scoreboard_frame, text=f"Game {i+1}: {score} points").grid(row=i+1, column=0, pady=2)
        
        ttk.Button(scoreboard_frame, text="Back", command=self.create_welcome_screen).grid(row=len(self.previous_scores)+1, column=0, pady=10)
    
    def start_todays_challenge(self):
        self.root.destroy()  # Close the current UI
        subprocess.Popen([sys.executable, "grid.py"])  # Open grid.py in a new process
    
    def load_previous_scores(self):
        try:
            with open("scoreboard.txt", "r") as f:
                self.previous_scores = [int(line.strip()) for line in f.readlines()]
        except:
            self.previous_scores = []
    
    def save_previous_scores(self):
        with open("scoreboard.txt", "w") as f:
            for score in self.previous_scores:
                f.write(f"{score}\n")

if __name__ == "__main__":
    root = tk.Tk()
    game = NQueensUI(root)
    root.mainloop()
