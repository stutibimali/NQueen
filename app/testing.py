from sklearn.metrics import f1_score, accuracy_score
from solution import backtracking_solver
import os
import pickle

def generate_true_labels(board_size):
    solution = backtracking_solver(board_size)
    return solution  # Each index is row, each value is correct column


def evaluate_ml_model(board_size):
    model_path = os.path.join("..", "models", f"model_{board_size}x{board_size}.pkl")
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("Model not found.")
        return

    X_test = [[i, board_size, i % 2, i // 2] for i in range(board_size)]  
    y_true = generate_true_labels(board_size)  
    y_pred = model.predict(X_test)

    f1 = f1_score(y_true, y_pred, average='macro')
    acc = accuracy_score(y_true, y_pred)

    print(f"F1 Score (macro): {f1:.2f}")
    print(f"Accuracy: {acc:.2f}")
