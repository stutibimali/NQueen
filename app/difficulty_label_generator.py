import os
import pandas as pd
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DATA_DIR

def assign_difficulty(board_size, time_taken):
    if board_size <= 5 and time_taken < 30:
        return "Easy"
    elif board_size <= 9 and time_taken < 60:
        return "Medium"
    else:
        return "Hard"

def generate_difficulty_csv():
    scoreboard_path = os.path.join(DATA_DIR, "scoreboard.txt")
    output_path = os.path.join(DATA_DIR, "difficulty_data.csv")
    
    if not os.path.exists(scoreboard_path):
        print("❌ No scoreboard.txt found.")
        return
    
    rows = []
    with open(scoreboard_path, "r") as f:
        for line in f:
            try:
                parts = line.strip().split(" - ")
                board_info = parts[1]  # e.g., 6x6
                time_taken = int(parts[2].replace("Time: ", "").replace("s", ""))
                board_size = int(board_info.split("x")[0])
                difficulty = assign_difficulty(board_size, time_taken)
                rows.append((board_size, time_taken, difficulty))
            except Exception as e:
                print(f"Skipping line: {line.strip()} - Error: {e}")

    df = pd.DataFrame(rows, columns=["board_size", "time_taken", "difficulty"])
    df.to_csv(output_path, index=False)
    print(f"✅ Saved difficulty dataset to {output_path}")

if __name__ == "__main__":
    generate_difficulty_csv()
