import tkinter as tk
from tkinter import ttk
import time
from grid import GridGenerator
from solution import generate_nqueens_solution
import random
from datetime import datetime, timedelta


class NQueensGame:
    def __init__(self, root):
        self.root = root
        self.root.title("♛ N-Queens ML Challenge")
        self.start_time = None
        self.timer_label = None
        self.canvas = None
        self.previous_scores = []
        self.queen_positions = {}
        self.error_label = None
        self.game_active = True
        self.original_colors = {}
        self.level = 1
        self.load_scores()
        self.show_loading_screen()
        self.root.after(2000, self.show_welcome_screen)

    def show_loading_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)
        ttk.Label(frame, text="🧠 Loading N-Queens ML Engine...", font=("Arial", 16)).pack(pady=30)
        progress = ttk.Progressbar(frame, mode='indeterminate')
        progress.pack(pady=20)
        progress.start(10)

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

        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)

        ttk.Label(frame, text="♛ N-Queens ML Challenge", font=("Arial", 22, "bold")).pack(pady=20)
        ttk.Button(frame, text="▶ Start Game", command=self.start_game).pack(pady=10)
        ttk.Button(frame, text="📊 View Scoreboard", command=self.show_scoreboard).pack(pady=10)

    def show_scoreboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)

        ttk.Label(frame, text="📋 Scoreboard", font=("Arial", 18)).pack(pady=10)
        for score in self.previous_scores:
            ttk.Label(frame, text=score, font=("Arial", 12)).pack()

        ttk.Button(frame, text="🔙 Back", command=self.show_welcome_screen).pack(pady=20)

    def start_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set board size based on level
        if self.level <= 3:
            self.board_size = 4
        elif self.level <= 6:
            self.board_size = 6
        elif self.level <= 9:
            self.board_size = 8
        else:
            self.board_size = 10

        # Setup colors
        self.colors = random.sample(
            ["red", "green", "blue", "yellow", "purple", "cyan", "magenta", "orange"],
            self.board_size
        )

        # Generate grid and solution
        self.solution = generate_nqueens_solution(self.board_size, use_ml=True, seed=self.level)
        self.grid_generator = GridGenerator(self.board_size, self.colors)
        self.grid = self.grid_generator.generate_grid(self.solution)

        # Setup time and game state
        self.time_limit = max(60 - (self.level - 1) * 5, 30)  # 30 sec min
        self.start_time = time.time()
        self.queen_positions = {}
        self.game_active = True
        self.original_colors = {}

        # UI Frame and Widgets
        frame = ttk.Frame(self.root, padding="20")
        frame.pack()

        ttk.Label(frame, text=f"🎮 Level {self.level}", font=("Arial", 14)).pack(pady=5)

        self.timer_label = ttk.Label(frame, text="Time Left: 0s", font=("Arial", 12))
        self.timer_label.pack(pady=5)

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
            remaining = self.time_limit - elapsed
            if remaining <= 0:
                self.end_game(failed=True)
            else:
                self.timer_label.config(text=f"Time Left: {remaining}s")
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
            if r == row or c == col or (abs(r - row)==1 and  abs(c - col)==1):
                return False
        return True

    def end_game(self,failed=False):
        self.game_active = False
        elapsed_time = int(time.time() - self.start_time)
        today = self.get_today_date()
        if not failed:
            self.level +=1
            elapsed_time = int(time.time() - self.start_time)
            today = self.get_today_date()
            score_entry = f"{today} - Time: {elapsed_time}s"
            self.previous_scores.append(score_entry)
            self.save_scores()
            streak = self.update_streak_data()
            self.show_completion_screen(time_taken=elapsed_time, streak=streak, failed=False)
        else:
            self.show_completion_screen(time_taken=elapsed_time, streak=None, failed=True)

    def get_today_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def load_streak_data(self):
        try:
            with open("streak.txt", "r") as f:
                data = f.read().strip().split(",")
                last_date = data[0]
                streak = int(data[1])
                return last_date, streak
        except FileNotFoundError:
            return "", 0

    def update_streak_data(self):
        today = self.get_today_date()
        last_date, streak = self.load_streak_data()
        if last_date == today:
            return streak
        elif last_date == (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"):
            streak += 1
        else:
            streak = 1
        with open("streak.txt", "w") as f:
            f.write(f"{today},{streak}")
        return streak

    def get_today_times(self):
        today = self.get_today_date()
        times = []
        for score in self.previous_scores:
            if score.startswith(today):
                times.append(int(score.split("Time: ")[1].replace("s", "")))
        return times

    def show_completion_screen(self, time_taken, streak=None,failed=False):
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)
        if failed:
            ttk.Label(frame, text="❌ Level Failed", font=("Arial", 20, "bold"), foreground="red").pack(pady=10)
            ttk.Label(frame, text=f"⏱️ Time: {time_taken}s", font=("Arial", 14)).pack(pady=5)
            ttk.Label(frame, text="Try Again!", font=("Arial", 12, "italic")).pack(pady=5)
        else:
            ttk.Label(frame, text="👑 You're crushing it!", font=("Arial", 20, "bold")).pack(pady=10)
            ttk.Label(frame, text=f"Queens placed! 🕐 {time_taken}s", font=("Arial", 14)).pack(pady=5)
            today_times = self.get_today_times()
            avg_time = sum(today_times) // len(today_times) if today_times else 0
            ttk.Label(frame, text=f"Today's Avg: {avg_time}s", font=("Arial", 12, "italic")).pack(pady=5)
            ttk.Label(frame, text=f"🔥 Current Streak: {streak} day{'s' if streak > 1 else ''}", font=("Arial", 12)).pack(pady=10)
        ttk.Button(frame, text="🔁 Play Again", command=self.start_game).pack(pady=5)
        ttk.Button(frame, text="🏠 Back to Home", command=self.show_welcome_screen).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGame(root)
    root.mainloop()
