import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def generate_nqueens_solution(board_size, use_ml=False):
    if use_ml:
        return ml_nqueens_solver(board_size)

    def is_safe(queens, row, col):
        for r in range(row):
            c = queens[r]
            if c == col or (abs(row - r) ==1 and abs(col - c)==1):
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
    return model.predict(X_test).tolist()

if __name__ == "__main__":
    board_size = 8
    use_ml = True
    solution = generate_nqueens_solution(board_size, use_ml=use_ml)
    print("Generated N-Queens Solution:", solution)
