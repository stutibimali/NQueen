import random

def generate_nqueens_solution(board_size):
    def is_safe(queens, row, col):
        for r in range(row):
            c = queens[r]
            if c == col or abs(row - r) == abs(col - c):
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

if __name__ == "__main__":
    board_size = 8  # Adjust as needed
    solution = generate_nqueens_solution(board_size)
    print("Generated N-Queens Solution:", solution)