# test_ml_solver.py
from solution import ml_nqueens_solver

def test_ml_solution(board_size):
    print(f"🔍 Testing ML solver for board size {board_size}x{board_size}")
    solution = ml_nqueens_solver(board_size)
    if solution:
        print(f"✅ ML Prediction: {solution}")
    else:
        print("❌ ML failed or model not found.")

if __name__ == "__main__":
    for size in range(4, 14):  # Test from 4x4 to 8x8
        test_ml_solution(size)
        print("-" * 40)
