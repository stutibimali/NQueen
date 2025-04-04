import tkinter as tk
from tkinter import ttk
import time
from grid import GridGenerator
from solution import generate_nqueens_solution
import random

class NQueensGame:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Challenge")
        self.start_time = None
        self.timer_label = None
        self.canvas = None
        self.previous_scores = []
        self.queen_positions = {}
        self.error_label = None
        self.game_active = True
        self.original_colors = {}

        self.load_scores()
        self.show_welcome_screen()

    def load_scores(self):
        try:
            with open("scoreboard.txt", "r") as f:
                self.previous_scores = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            self.previous_scores = []

    def save_scores(self):
        with open("scoreboard.txt", "w") as f:
            for score in self.previous_scores:
                f.write(score + "\n")

    def show_welcome_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame, text="Welcome to the N-Queens Challenge!", font=("Arial", 16)).pack(pady=10)
        ttk.Button(frame, text="Start Game", command=self.start_game).pack(pady=10)
        ttk.Button(frame, text="View Scoreboard", command=self.show_scoreboard).pack(pady=10)

    def show_scoreboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame, text="Scoreboard", font=("Arial", 16)).pack(pady=10)
        for score in self.previous_scores:
            ttk.Label(frame, text=score).pack()

        ttk.Button(frame, text="Back", command=self.show_welcome_screen).pack(pady=10)

    def start_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.board_size = random.choice([4, 6, 8])
        self.colors = random.sample(["red", "green", "blue", "yellow", "purple", "cyan", "magenta", "orange"], self.board_size)
        self.solution = generate_nqueens_solution(self.board_size)
        self.grid_generator = GridGenerator(self.board_size, self.colors)
        self.grid = self.grid_generator.generate_grid(self.solution)
        self.start_time = time.time()
        self.queen_positions = {}
        self.game_active = True
        self.original_colors = {}

        frame = ttk.Frame(self.root, padding="10")
        frame.pack()

        self.timer_label = ttk.Label(frame, text="Time: 0s", font=("Arial", 12))
        self.timer_label.pack(pady=5)
        self.update_timer()

        self.error_label = ttk.Label(frame, text="", font=("Arial", 12), foreground="red")
        self.error_label.pack(pady=5)

        self.canvas = tk.Canvas(frame, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.place_queen)
        self.canvas.bind("<Double-Button-1>", self.remove_queen)

        self.display_grid()

    def update_timer(self):
        if self.start_time and self.game_active:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def display_grid(self):
        self.canvas.delete("all")
        cell_size = 400 // self.board_size

        for i in range(self.board_size):
            for j in range(self.board_size):
                color = self.grid[i][j]
                self.canvas.create_rectangle(
                    j * cell_size, i * cell_size,
                    (j+1) * cell_size, (i+1) * cell_size,
                    fill=color, outline="black"
                )
                if (i, j) in self.queen_positions:
                    text = "Q" if self.queen_positions[(i, j)] else "✖"
                    self.canvas.create_text(
                        j * cell_size + cell_size//2, i * cell_size + cell_size//2,
                        text=text, font=("Arial", 16, "bold"),
                        fill="black" if self.queen_positions[(i, j)] else "white"
                    )
        if len(self.queen_positions) == self.board_size and all(self.queen_positions.values()):
            self.end_game()

    def place_queen(self, event):
        if not self.game_active:
            return
        cell_size = 400 // self.board_size
        row = event.y // cell_size
        col = event.x // cell_size

        if (row, col) in self.queen_positions:
            return

        valid = self.is_valid_placement(row, col)
        self.queen_positions[(row, col)] = valid
        self.error_label.config(text="" if valid else "Invalid placement!")
        self.display_grid()

    def remove_queen(self, event):
        if not self.game_active:
            return
        cell_size = 400 // self.board_size
        row = event.y // cell_size
        col = event.x // cell_size

        if (row, col) in self.queen_positions:
            del self.queen_positions[(row, col)]
            self.error_label.config(text="")
            self.display_grid()

    def is_valid_placement(self, row, col):
        for (r, c), valid in self.queen_positions.items():
            if r == row or c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def end_game(self):
        self.game_active = False
        elapsed_time = int(time.time() - self.start_time)
        self.error_label.config(text=f"Congratulations! You completed the challenge in {elapsed_time}s", foreground="green")
        self.previous_scores.append(f"Time: {elapsed_time}s")
        self.save_scores()
        self.start_time = None

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGame(root)
    root.mainloop()
