import numpy as np
import pickle
from solution import backtracking_solver
import os
import random
def generate_training_data(board_size, n_samples=1000, noise_prob=0.15):
    X, y = [], []
    for _ in range(n_samples):
        solution = backtracking_solver(board_size)
        for row, col in enumerate(solution):
            features = [row, board_size, row % 2, row // 2]
            if random.random() < noise_prob:
                # Introduce noise: assign a wrong column for this row
                wrong_cols = [c for c in range(board_size) if c != col]
                col = random.choice(wrong_cols)
            X.append(features)
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

def generate_move_recommendation_data(board_size, n_samples=10000):
    X, y = [], []
    for _ in range(n_samples):
        solution = backtracking_solver(board_size)
        partial_state = [-1] * board_size
        for row in range(board_size):
            col = solution[row]
            features = partial_state[:row] + [-1] * (board_size - row)
            features.append(row)  # current row as a feature
            X.append(features)
            y.append(col)
            partial_state[row] = col
    return np.array(X), np.array(y)

def train_move_recommender_model(board_size):
    from sklearn.ensemble import RandomForestClassifier
    X, y = generate_move_recommendation_data(board_size)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    os.makedirs("../models", exist_ok=True)
    with open(f"../models/move_recommender_{board_size}.pkl", "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Move recommender model saved for {board_size}x{board_size}")

for size in range(4, 15):
    train_move_recommender_model(size)
