import tkinter as tk
import random
from datetime import datetime
from solution import generate_nqueens_solution

class GridGenerator:
    def __init__(self, board_size, colors,seed=None):
        self.board_size = board_size
        self.colors = colors
        self.seed = seed
        self.color_grid = [[None for _ in range(board_size)] for _ in range(board_size)]
        if seed is not None:
            random.seed(seed)
    def generate_grid(self, solution):
        current_date = datetime.now().strftime("%Y%m%d")
        random.seed()
        color_assignment = {}
        used_colors = set()
        
        # Assign a unique color to each queen
        for row in range(self.board_size):
            col = solution[row]
            if len(used_colors) == len(self.colors):
                # If not enough unique colors, reuse from full list
                color = random.choice(self.colors)
            else:
                available_colors = [c for c in self.colors if c not in used_colors]
                color = random.choice(available_colors)

            self.color_grid[row][col] = color
            color_assignment[(row, col)] = color
            used_colors.add(color)

        # Grow each color block around its queen
        for (row, col), color in color_assignment.items():
            self.grow_color_block(row, col, color)

        self.fill_remaining_cells()
        return self.color_grid

    def grow_color_block(self, row, col, color):
        queue = [(row, col)]
        max_cells = random.randint(3, self.board_size * 2)
        filled = 0

        while queue and filled < max_cells:
            current = queue.pop(0)
            for ni, nj in [(current[0]-1, current[1]), (current[0]+1, current[1]),
                           (current[0], current[1]-1), (current[0], current[1]+1)]:
                if (0 <= ni < self.board_size and 0 <= nj < self.board_size and 
                    self.color_grid[ni][nj] is None):
                    self.color_grid[ni][nj] = color
                    queue.append((ni, nj))
                    filled += 1

    def fill_remaining_cells(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.color_grid[i][j] is None:
                    neighbors = [self.color_grid[ni][nj] for ni, nj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                                 if 0 <= ni < self.board_size and 0 <= nj < self.board_size and self.color_grid[ni][nj]]
                    self.color_grid[i][j] = random.choice(neighbors) if neighbors else random.choice(self.colors)

class NQueensUI:
    def __init__(self, root):
        self.streak = self.load_streak()  # You should track it already
        self.board_size = min(4 + self.streak, 14)  # Cap at 14x14 to avoid crazy boards
        self.root = root
        import colorsys

        def generate_distinct_colors(n):
            colors = []
            for i in range(n):
                hue = i / n
                r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                colors.append(f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}')
            return colors

        self.colors = generate_distinct_colors(self.board_size)

        self.solution = generate_nqueens_solution(self.board_size)
        self.grid_generator = GridGenerator(self.board_size, self.colors)
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
    app = NQueensUI(root)
    root.mainloop()