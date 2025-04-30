import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict
import pickle
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import MODEL_DIR

def generate_nqueens_solution(board_size, use_ml=True, use_rl=False, seed=None):
    if seed is not None:
        random.seed(seed)
    if use_rl:
        solution = rl_nqueens_solver(board_size)
        if solution and is_valid_solution(solution):
            return solution
    if use_ml:
        solution = ml_nqueens_solver(board_size)
        if solution and is_valid_solution(solution):
            return solution
    return backtracking_solver(board_size)

def is_valid_solution(queens):
    board_size = len(queens)
    for r1 in range(board_size):
        for r2 in range(r1 + 1, board_size):
            c1, c2 = queens[r1], queens[r2]
            if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True

def recommend_move(partial_board, board_size):
    model_path = os.path.join("..", "models", f"move_recommender_{board_size}.pkl")
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        return None

    row = sum([1 for x in partial_board if x != -1])
    features = partial_board[:row] + [-1] * (board_size - row)
    features.append(row)
    pred = model.predict([features])
    return pred[0]

def backtracking_solver(board_size):
    def is_safe(queens, row, col):
        for r in range(row):
            c = queens[r]
            if c == col or abs(row - r) == 1 and abs(col - c) == 1:
                return False
        return True

    def solve(row=0, queens=[]):
        if row == board_size:
            return queens[:]
        for col in range(board_size):
            if col not in queens and is_safe(queens, row, col):
                queens.append(col)
                result = solve(row + 1, queens)
                if result:
                    return result
                queens.pop()
        return None

    solution = solve()
    if solution is None:
        raise Exception("No valid solution found")
    return solution

def ml_nqueens_solver(board_size):
    model_path = os.path.join("..", "models", f"model_{board_size}x{board_size}.pkl")
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        return None, []

    X_test = [[i, board_size, i % 2, i // 2] for i in range(board_size)]
    prediction = model.predict(X_test)

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X_test)
        confidences = [max(row) for row in probs]
    else:
        confidences = [1.0] * board_size

    if len(set(prediction)) < board_size:
        return None, []

    return prediction.tolist(), confidences

def rl_nqueens_solver(board_size):
    Q = defaultdict(float)
    alpha = 0.1
    gamma = 0.9
    episodes = 5000

    def get_state_key(state):
        return tuple(state)

    def is_valid(state, row, col):
        for r in range(row):
            if state[r] == col or abs(r - row) == abs(state[r] - col):
                return False
        return True

    for _ in range(episodes):
        state = [-1] * board_size
        for row in range(board_size):
            actions = [c for c in range(board_size) if is_valid(state, row, c)]
            if not actions:
                break
            action = random.choice(actions)
            next_state = state[:]
            next_state[row] = action
            reward = 1 if is_valid(next_state, row, action) else -10
            Q[(get_state_key(state), action)] += alpha * (reward + gamma * max(
                Q.get((get_state_key(next_state), a), 0) for a in range(board_size)) - Q[(get_state_key(state), action)])
            state = next_state

    state = [-1] * board_size
    for row in range(board_size):
        valid_actions = [(action, Q[(get_state_key(state), action)])
                         for action in range(board_size) if is_valid(state, row, action)]
        if not valid_actions:
            return None
        best_action = max(valid_actions, key=lambda x: x[1])[0]
        state[row] = best_action

    return state
