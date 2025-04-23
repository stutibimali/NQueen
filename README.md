# ♛ N-Queens ML Challenge

An intelligent N-Queens puzzle solver that combines **Machine Learning (ML)** and **Reinforcement Learning (RL)** with a polished Tkinter UI for a daily evolving challenge.

---

## 🎯 Objective

Place `N` queens on an `N x N` board such that no two queens threaten each other — not in the same row, column, or diagonal.

This project includes:
- ✅ Intelligent board generation using ML (with RL fallback)
- ✅ Difficulty scaling based on player streaks
- ✅ Dynamic timer and color-clustered grid
- ✅ Daily challenge logic with streak tracking
- ✅ Polished UI with crown icons and music

---

## 🧠 Machine Learning (ML) Used

### ✅ Algorithm
- **Model**: `RandomForestClassifier`
- **Library**: `scikit-learn`

### 📊 Data Generation
- Uses `backtracking_solver()` to generate valid solutions for each board size (from 4x4 to 14x14).
- For each queen placement:
  - Input features (`X`): `[row_index, board_size, row % 2, row // 2]`
    - `row_index`: the row number (0-based)
    - `board_size`: the size of the current board
    - `row % 2`: parity feature (even/odd)
    - `row // 2`: progression grouping
  - Target (`y`): column index where the queen is placed

### 🧠 Model Training
- Each board size has its own model: `model_4x4.pkl`, ..., `model_14x14.pkl`
- Trained using:
  ```python
  RandomForestClassifier(n_estimators=100, random_state=42)
  ```

### ✅ Prediction Flow
- During gameplay, the model:
  - Loads the `.pkl` file corresponding to the board size
  - Predicts queen column per row
  - Validates if output is a proper permutation
- Optional: Displays per-row confidence via `predict_proba`

---

## 🤖 Reinforcement Learning (RL) Used

### ✅ Q-Learning (model-free)
- Learns from scratch using trial and error (5000 episodes)
- State = current board (partial solution), Action = column placement
- Reward:
  - `+1` for valid placement
  - `-10` for conflicts
- Bellman update rule with:
  - `alpha = 0.1`
  - `gamma = 0.9`
- RL is only used when ML fails or returns an invalid solution


---

## 🕹 Game Features

- 🎨 Colorful board with queen-centric color blocks
- 👑 Crown icons for queens and conflict indicators
- 🕒 Timer adjusts with board size
- 🔁 Replay option and leaderboard
- 🔥 Daily streak mechanic with progressive challenge
- 🎵 Background music and sound effects

---

## 🛠 Project Structure

```
NQueen/
├── app/
│   ├── main.py
│   ├── ui.py
│   ├── grid.py
│   ├── solution.py
|   ├── ml_data_generator.py    # ML model training script
|   ├── test_ml_solver.py       # Terminal-based ML testing
├── config.py
├── .gitignore
├── .venv
├── models/                 # Trained ML models
├── data/                   # Scoreboards and streak files
├── music/                  # Game music
├── assests/                # images 
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 📦 Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

---

### ▶️ Run the Game (Tkinter)

```bash
python app/main.py
```

Before playing, generate models:

```bash
python ml_data_generator.py
```

---

## 🔍 Test ML Predictions (Terminal)

```bash
python test_ml_solver.py
```

Prints predictions with per-row confidence from the ML model.

---

## 📁 Output Files

| File                | Purpose                        |
|---------------------|--------------------------------|
| `scoreboard.txt`    | Tracks completed levels        |
| `streak.txt`        | Stores daily streak data       |
| `highscores.txt`    | Best times per board size      |
| `models/*.pkl`      | ML models (1 per board size)   |

---

## 🙌 Built By

Developed by a Data Science Master's students.  
This project demonstrates **practical ML deployment**, daily challenge logic, and clean UI/UX design.

---

## 📌 Future Work

- [ ] Online scoreboard and login
- [ ] Drag-and-drop version for Android (via Flutter or Kivy)
- [ ] Visualize ML vs RL performance
- [ ] Deploy web version via Flask/Render

---

**Solve puzzles with the power of ML and logic!♛**



---

## © License & Copyright

© 2025 N-Queens ML Challenge Team. All rights reserved.

This project was developed collaboratively by a group of graduate students as part of a Machine Learning coursework project.

You are welcome to use or reference this project for **educational and non-commercial purposes only**.  
Redistribution or commercial use without written permission is prohibited.

Team Members:
- Stuti Bimali  
- Hrishabh Mahaju
- Binaya Dhakal
- Aayush Dongol

---