import tkinter as tk
import random
from datetime import datetime
from solution import generate_nqueens_solution

class GridGenerator:
    def __init__(self, board_size, colors):
        self.board_size = board_size
        self.colors = colors
        self.color_grid = [[None for _ in range(board_size)] for _ in range(board_size)]

    def generate_grid(self, solution):
        current_date = datetime.now().strftime("%Y%m%d")
        random.seed(current_date)
        color_assignment = {}
        used_colors = set()

        # Assign unique color to each queen position
        for row in range(self.board_size):
            col = solution[row]
            available_colors = [c for c in self.colors if c not in used_colors]
            color = random.choice(available_colors)
            self.color_grid[row][col] = color
            color_assignment[(row, col)] = color
            used_colors.add(color)

        # Grow each region from queen positions to form color blocks
        for (row, col), color in color_assignment.items():
            self.grow_region(row, col, color, solution)

        self.fill_uncolored_cells()
        return self.color_grid

    def grow_region(self, start_row, start_col, color, solution):
        queue = [(start_row, start_col)]
        filled = 0
        max_fill = random.randint(3, self.board_size * 2)

        while queue and filled < max_fill:
            row, col = queue.pop(0)
            if self.color_grid[row][col] != color:
                continue
            filled += 1

            for ni, nj in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
                if (0 <= ni < self.board_size and 0 <= nj < self.board_size and
                    self.color_grid[ni][nj] is None and (ni, nj) not in solution):
                    self.color_grid[ni][nj] = color
                    queue.append((ni, nj))

    def fill_uncolored_cells(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.color_grid[i][j] is None:
                    neighbors = [self.color_grid[ni][nj] for ni, nj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)] 
                                 if 0 <= ni < self.board_size and 0 <= nj < self.board_size and self.color_grid[ni][nj]]
                    if neighbors:
                        self.color_grid[i][j] = random.choice(neighbors)
                    else:
                        self.color_grid[i][j] = random.choice(self.colors)

class NQueensUI:
    def __init__(self, root, board_size=8):
        self.root = root
        self.board_size = board_size
        self.colors = ["red", "green", "blue", "yellow", "purple", "cyan", "magenta", "orange"]

        self.solution = generate_nqueens_solution(self.board_size)
        self.grid_generator = GridGenerator(board_size, self.colors)
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.display_grid()

    def display_grid(self):
        self.canvas.delete("all")
        cell_size = 400 // self.board_size
        grid = self.grid_generator.generate_grid(self.solution)

        for i in range(self.board_size):
            for j in range(self.board_size):
                color = grid[i][j]
                self.canvas.create_rectangle(
                    j * cell_size, i * cell_size,
                    (j+1) * cell_size, (i+1) * cell_size,
                    fill=color, outline="black"
                )
                if j == self.solution[i]:
                    self.canvas.create_text(
                        j * cell_size + cell_size//2, i * cell_size + cell_size//2,
                        text="Q", font=("Arial", 16, "bold"), fill="black"
                    )

if __name__ == "__main__":
    root = tk.Tk()
    root.title("N-Queens Grid")
    app = NQueensUI(root, board_size=8)
    root.mainloop()