import tkinter as tk
from tkinter import ttk
import time
import sys
import pygame
from grid import GridGenerator
from solution import generate_nqueens_solution
import random
from datetime import datetime, timedelta
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DATA_DIR
from solution import ml_nqueens_solver
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from solution import recommend_move
from utils_difficulty import predict_difficulty
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
        self.play_music = True
        self.confidences = []
        self.recommendations = []  # row: recommended col
        self.mistakes = []         # list of (row, placed_col, recommended_col)
        self.mistake_rows = set()
        self.user_moves = []

        self.crown_image = ImageTk.PhotoImage(Image.open("../assets/crown.png").resize((32, 32)))
        self.crownconflict_image = ImageTk.PhotoImage(Image.open("../assets/swords.png").resize((32, 32)))
        pygame.mixer.init()
        if self.play_music:
            pygame.mixer.music.load("../music/Just Getting Started.mp3")
            pygame.mixer.music.play(-1)
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
    
    def show_analysis_graph(self):
        if not hasattr(self, "recommendations") or not self.recommendations:
            print("⚠️ No move data to analyze.")
            return

        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("📊 ML Move Analysis")

        frame = ttk.Frame(analysis_window, padding=10)
        frame.pack(fill="both", expand=True)

        # === Plot 1: Confidence vs Mistake ===
        fig1, ax1 = plt.subplots(figsize=(6, 3.5))
        rows = list(range(len(self.confidences)))
        ax1.plot(rows, self.confidences, label="Confidence", marker="o", color="blue")
        
        for idx in self.mistake_rows:
            if idx < len(self.confidences):
                ax1.plot(idx, self.confidences[idx], marker="x", color="red", markersize=10, label="Mistake" if idx == list(self.mistake_rows)[0] else "")

        ax1.set_ylim(0, 1)
        ax1.set_title("Confidence & Mistake Highlight")
        ax1.set_xlabel("Row")
        ax1.set_ylabel("Confidence")
        ax1.legend()

        canvas1 = FigureCanvasTkAgg(fig1, master=frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(pady=10)

        # === Plot 2: Actual vs Recommended ===
        fig2, ax2 = plt.subplots(figsize=(6, 3.5))
        rows = list(range(len(self.user_moves)))
        actual = [col for _, col in self.user_moves]
        recommended = [col for _, col in self.recommendations[:len(self.user_moves)]]

        ax2.plot(rows, recommended, label="Recommended", marker="o", color="green")
        ax2.plot(rows, actual, label="Your Move", marker="x", color="orange")
        ax2.set_title("Your Move vs ML Recommendation")
        ax2.set_xlabel("Row")
        ax2.set_ylabel("Column")
        ax2.legend()
        ax2.grid(True)

        canvas2 = FigureCanvasTkAgg(fig2, master=frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(pady=10)

    def load_scores(self):
        path = os.path.join(DATA_DIR, "scoreboard.txt")
        try:
            with open(path, "r") as f:
                self.previous_scores = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            self.previous_scores = []


    def save_scores(self):
        path = os.path.join(DATA_DIR, "scoreboard.txt")
        with open(path, "w") as f:
            for score in self.previous_scores:
                f.write(score + "\n")

    def load_high_scores(self):
        path = os.path.join(DATA_DIR, "highscores.txt")
        try:
            with open(path, "r") as f:
                return {int(line.split(":")[0]): int(line.split(":")[1].replace("s", "").strip()) for line in f.readlines()}
        except FileNotFoundError:
            return {}

    def save_high_score(self, board_size, time_taken):
        high_scores = self.load_high_scores()
        high_scores[board_size] = time_taken
        path = os.path.join(DATA_DIR, "highscores.txt")
        with open(path, "w") as f:
            for level, time_ in sorted(high_scores.items()):
                f.write(f"{level}: {time_}s\n")

    def show_welcome_screen(self):
        if self.play_music:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("../music/Just Getting Started.mp3")
            pygame.mixer.music.play(-1)
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)
        ttk.Label(frame, text="♛ N-Queens ML Challenge", font=("Arial", 22, "bold")).pack(pady=20)
        ttk.Button(frame, text="▶ Start Game", command=self.start_game).pack(pady=10)
        ttk.Button(frame, text="📊 View Scoreboard", command=self.show_scoreboard).pack(pady=10)
        ttk.Button(frame, text="⚙ Settings", command=self.show_settings_screen).pack(pady=10)

    def show_settings_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)
        ttk.Label(frame, text="🎵 Settings", font=("Arial", 18, "bold")).pack(pady=20)
        ttk.Label(frame, text="Background Audio:", font=("Arial", 12)).pack(pady=5)

        def toggle_audio():
            self.play_music = not self.play_music
            if self.play_music:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            audio_button.config(text="On" if self.play_music else "Off")

        audio_button = ttk.Button(frame, text="On" if self.play_music else "Off", command=toggle_audio)
        audio_button.pack(pady=5)
        ttk.Button(frame, text="🔙 Back to Home", command=self.show_welcome_screen).pack(pady=20)

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
        if self.play_music:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("../music/gamesound.mp3")
            pygame.mixer.music.play(-1)
        for widget in self.root.winfo_children():
            widget.destroy()

        self.board_size = random.randint(4, 14)
        self.level = self.board_size
        import colorsys

        def generate_distinct_colors(n):
            colors = []
            for i in range(n):
                hue = i / n
                r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                colors.append(f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}')
            return colors

        self.colors = random.sample(generate_distinct_colors(self.board_size),min(self.board_size, 14))
        self.solution, self.confidences = ml_nqueens_solver(self.board_size)
        if self.solution is None:
            self.solution = generate_nqueens_solution(self.board_size, use_ml=False, use_rl=True)
            self.confidences = [0.0] * self.board_size
        self.mistake_rows = set()
        self.user_moves = []
        self.recommendations = [(i, col) for i, col in enumerate(self.solution)]
        self.mistakes = [False] * self.board_size

        self.grid_generator = GridGenerator(self.board_size, self.colors, seed=random.randint(0, 100000))
        self.grid = self.grid_generator.generate_grid(self.solution)

        self.time_limit = max(90 - (self.board_size * 3), 30)
        self.start_time = time.time()
        self.queen_positions = {}
        self.game_active = True
        self.original_colors = {}

        frame = ttk.Frame(self.root, padding="20")
        frame.pack()

        ttk.Label(frame, text=f"🎮 Level {self.level} - {self.board_size}x{self.board_size}", font=("Arial", 14)).pack(pady=5)
        self.timer_label = ttk.Label(frame, text="Time Left: 0s", font=("Arial", 12))
        self.timer_label.pack(pady=5)
        self.error_label = ttk.Label(frame, text="", font=("Arial", 12), foreground="red")
        self.error_label.pack(pady=5)

        self.canvas = tk.Canvas(frame, width=400, height=400)
        self.canvas.pack()

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="🧹 Clear", command=self.clear_board).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🔙 Back", command=self.show_welcome_screen).pack(side="left", padx=5)

        self.canvas.bind("<Button-1>", self.place_queen)
        self.canvas.bind("<Double-Button-1>", self.remove_queen)

        self.display_grid()
        self.update_timer()

    def update_timer(self):
        if self.start_time and self.game_active:
            elapsed = int(time.time() - self.start_time)
            remaining = self.time_limit - elapsed
            if remaining <= 0:
                self.end_game(failed=True)
            else:
                try:
                    if self.timer_label.winfo_exists():
                        self.timer_label.config(text=f"Time Left: {remaining}s")
                except tk.TclError:
                    return
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
                    if self.queen_positions[(i, j)]:
                        self.canvas.create_image(
                            j * cell_size + cell_size // 2,
                            i * cell_size + cell_size // 2,
                            image=self.crown_image,
                            anchor="center"
                        )
                    else:
                        self.canvas.create_image(
                            j * cell_size + cell_size // 2,
                            i * cell_size + cell_size // 2,
                            image= self.crownconflict_image, 
                            anchor='center'
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
        self.user_moves.append((row, col))  # Record actual move

        # ✅ Use initial ML recommendation from self.recommendations
        if self.recommendations and row < len(self.recommendations):
            predicted_col = self.recommendations[row][1]
            if predicted_col != col:
                self.mistakes.append((row, col, predicted_col))
                self.mistake_rows.add(row)

        # 🧠 Optionally compare with dynamic model recommendation
        partial = [-1] * self.board_size
        for (r, c), _ in self.queen_positions.items():
            partial[r] = c
        dynamic_recommended = recommend_move(partial, self.board_size)
        self.recommendations.append((row, dynamic_recommended))

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

    def clear_board(self):
        self.queen_positions = {}
        self.error_label.config(text="")
        self.display_grid()

    def is_valid_placement(self, row, col):
        for (r, c), valid in self.queen_positions.items():
            if r == row or c == col or (abs(r - row)==1 and abs(c - col)==1):
                return False
        return True

    def end_game(self, failed=False):
        self.game_active = False
        elapsed_time = int(time.time() - self.start_time)
        today = self.get_today_date()
        try:
            difficulty = predict_difficulty(self.board_size, elapsed_time)
            print(f"Predicted difficulty: {difficulty}")
        except Exception as e:
            print(f"Difficulty prediction failed: {e}")
            difficulty = "Unknown"

        new_record = False
        if not failed:
            score_entry = f"{today} - {self.board_size}x{self.board_size} - Time: {elapsed_time}s"
            self.previous_scores.append(score_entry)
            self.save_scores()

            high_scores = self.load_high_scores()
            prev_best = high_scores.get(self.board_size, None)
            if prev_best is None or elapsed_time < prev_best:
                self.save_high_score(self.board_size, elapsed_time)
                new_record = True

            streak = self.update_streak_data()
            self.show_completion_screen(elapsed_time, streak, failed=False, new_record=new_record)
        else:
            self.show_completion_screen(elapsed_time, None, failed=True)

    def get_today_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def load_streak_data(self):
        path = os.path.join(DATA_DIR, "streak.txt")
        try:
            with open(path, "r") as f:
                last_date, streak = f.read().strip().split(",")
                return last_date, int(streak)
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
        path = os.path.join(DATA_DIR, "streak.txt")
        with open(path, "w") as f:
            f.write(f"{today},{streak}")
        return streak

    def get_today_times(self):
        today = self.get_today_date()
        return [
            int(score.split("Time: ")[1].replace("s", ""))
            for score in self.previous_scores if score.startswith(today)
        ]

    def start_specific_game(self, board_size):
        if self.play_music:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("../music/gamesound.mp3")
            pygame.mixer.music.play(-1)
        for widget in self.root.winfo_children():
            widget.destroy()

        self.board_size = board_size
        self.level = board_size
        import colorsys

        def generate_distinct_colors(n):
            colors = []
            for i in range(n):
                hue = i / n
                r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                colors.append(f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}')
            return colors

        self.colors = random.sample(generate_distinct_colors(self.board_size), min(self.board_size, 14))
        self.solution, self.confidences = ml_nqueens_solver(self.board_size)
        if self.solution is None:
            self.solution = generate_nqueens_solution(self.board_size, use_ml=False, use_rl=True)
            self.confidences = [0.0] * self.board_size
        self.mistake_rows = set()
        self.grid_generator = GridGenerator(self.board_size, self.colors, seed=random.randint(0, 100000))
        self.grid = self.grid_generator.generate_grid(self.solution)

        self.time_limit = max(90 - (self.board_size * 3), 30)
        self.start_time = time.time()
        self.queen_positions = {}
        self.game_active = True
        self.original_colors = {}

        frame = ttk.Frame(self.root, padding="20")
        frame.pack()

        ttk.Label(frame, text=f"🎮 Level {self.level} - {self.board_size}x{self.board_size}", font=("Arial", 14)).pack(pady=5)
        self.timer_label = ttk.Label(frame, text="Time Left: 0s", font=("Arial", 12))
        self.timer_label.pack(pady=5)
        self.error_label = ttk.Label(frame, text="", font=("Arial", 12), foreground="red")
        self.error_label.pack(pady=5)

        self.canvas = tk.Canvas(frame, width=400, height=400)
        self.canvas.pack()

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="🧹 Clear", command=self.clear_board).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🔙 Back", command=self.show_welcome_screen).pack(side="left", padx=5)

        self.canvas.bind("<Button-1>", self.place_queen)
        self.canvas.bind("<Double-Button-1>", self.remove_queen)

        self.display_grid()
        self.update_timer()

    def show_completion_screen(self, time_taken, streak=None, failed=False, new_record=False):
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)
        if failed:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("../music/levelfailed.mp3")
            pygame.mixer.music.play()
            ttk.Label(frame, text="❌ Level Failed", font=("Arial", 20, "bold"), foreground="red").pack(pady=10)
            ttk.Label(frame, text=f"⏱️ Time: {time_taken}s", font=("Arial", 14)).pack(pady=5)
            ttk.Label(frame, text="Try Again or Start Fresh!", font=("Arial", 12, "italic")).pack(pady=10)

            def retry_same_level():
                self.start_specific_game(self.board_size)


            ttk.Button(frame, text="🔁 Try Same Level", command=retry_same_level).pack(pady=5)
        else:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("../music/Boss Clear.mp3")
            pygame.mixer.music.play()
            ttk.Label(frame, text="👑 You're crushing it!", font=("Arial", 20, "bold")).pack(pady=10)
            ttk.Label(frame, text=f"Queens placed! 🕐 {time_taken}s", font=("Arial", 14)).pack(pady=5)
            if new_record:
                ttk.Label(frame, text="🥇 New Record!", font=("Arial", 14), foreground="green").pack(pady=5)
            else:
                best = self.load_high_scores().get(self.board_size)
                if best:
                    ttk.Label(frame, text=f"🏆 Best Time: {best}s", font=("Arial", 12)).pack(pady=5)
            today_times = self.get_today_times()
            avg_time = sum(today_times) // len(today_times) if today_times else 0
            ttk.Label(frame, text=f"Today's Avg: {avg_time}s", font=("Arial", 12, "italic")).pack(pady=5)
            ttk.Label(frame, text=f"🔥 Current Streak: {streak} day{'s' if streak > 1 else ''}", font=("Arial", 12)).pack(pady=10)
        ttk.Button(frame, text="🔁 New Game", command=self.start_game).pack(pady=5)
        ttk.Button(frame, text="🏠 Back to Home", command=self.show_welcome_screen).pack(pady=5)
        ttk.Button(frame, text="🔍 Analyze Moves", command=self.show_analysis_graph).pack(pady=5)