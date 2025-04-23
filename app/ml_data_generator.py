import numpy as np
import pickle
from solution import backtracking_solver
import os

def generate_training_data(board_size, n_samples=1000):
    X, y = [], []
    for _ in range(n_samples):
        solution = backtracking_solver(board_size)
        for row, col in enumerate(solution):
            # Basic + engineered features: row, board size, parity, half
            X.append([row, board_size, row % 2, row // 2])
            y.append(col)
    return np.array(X), np.array(y)

def train_and_save_model(board_size):
    X, y = generate_training_data(board_size)
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    os.makedirs("../models", exist_ok=True)  # create if not exists
    with open(f"../models/model_{board_size}x{board_size}.pkl", "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Saved model for {board_size}x{board_size} to model_{board_size}x{board_size}.pkl")

# Example: train for 4x4 to 14x14
for size in range(4, 15):
    train_and_save_model(size)
