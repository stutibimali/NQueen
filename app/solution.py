import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict

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
    X_train = np.array([[i] for i in range(board_size)])
    y_train = np.random.permutation(board_size)

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)

    X_test = np.array([[i] for i in range(board_size)])
    prediction = model.predict(X_test)

    return prediction.tolist()

def rl_nqueens_solver(board_size):
    Q = defaultdict(float)
    episodes = 1000

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
            action = np.random.choice(actions)
            state[row] = action
            Q[(get_state_key(state), action)] += 1.0

    state = [-1] * board_size
    for row in range(board_size):
        valid_actions = [(action, Q[(get_state_key(state), action)])
                         for action in range(board_size) if is_valid(state, row, action)]
        if not valid_actions:
            return None
        best_action = max(valid_actions, key=lambda x: x[1])[0]
        state[row] = best_action

    return state
