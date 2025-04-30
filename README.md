# ♛ N-Queens ML Challenge

An AI-powered twist on the classic N-Queens puzzle — designed to be a daily brain-training game that combines **Machine Learning**, **Reinforcement Learning**, and an engaging, colorful UI. Developed as a final project for DSCI 6003 by a team of Data Science Master’s students.

---

## 🎯 Objective

Place `N` queens on an `N x N` board such that no two queens threaten each other — no two queens in the same row, column, or diagonal.

This daily-playable puzzle app includes:
- 🎓 ML-driven puzzle generation and move suggestions
- 🤖 RL-based fallback solver when ML fails
- 🔥 Dynamic difficulty scaling with streak tracking
- ⏳ Timed gameplay based on board size
- 🎨 Queen-centric color visualization with crown icons
- 🎵 Background music and themed sound effects

---

## 🧠 ML & RL Integration

### ✅ Machine Learning
**Goal**: Predict valid queen positions per row and difficulty levels based on solve time.

- **Model**: `RandomForestClassifier` per board size
- **Features**: `[row_index, board_size, row % 2, row // 2]`
- **Training Script**: `ml_data_generator.py`
- **Output**: 
  - `model_<size>x<size>.pkl` for solving
  - `move_recommender_<size>.pkl` for real-time suggestions

### 📊 Difficulty Prediction
- Labels: Easy, Medium, Hard (based on board size and time)
- Training: `train_difficulty_model.py` using `difficulty_data.csv`
- Real-time prediction in UI post-game

### 🤖 Reinforcement Learning (Fallback)
- Q-learning with:
  - State: partial board
  - Action: column placement
  - Reward: +1 valid, -10 conflict
- Used if ML model fails or gives invalid output

---

## 🕹️ Gameplay Features

| Feature                        | Description                                    |
|-------------------------------|------------------------------------------------|
| 👑 Crown Icons                | Replaces "Q" with themed icons                |
| 🎨 Colorful Zones             | Color clusters around queen positions        |
| 🎵 Audio System               | 3 modes: background, win, fail music          |
| 🔁 Retry + Streak Logic       | One level per day, progressive difficulty     |
| 📊 Analysis Panel             | Move vs ML recommendations, confidence graph  |
| 📈 Scoreboard + High Scores   | Tracks performance and personal records       |

---

## 🗂 Project Structure

```
NQueen/
├── app/
│   ├── main.py                # Entry point
│   ├── ui.py                  # Full UI + game logic
│   ├── grid.py                # Color + layout generator
│   ├── solution.py            # ML, RL, backtracking solvers
│   ├── ml_data_generator.py   # ML training script
│   ├── test_ml_solver.py      # CLI test utility
│   ├── difficulty_label_generator.py
│   ├── train_difficulty_model.py
│   └── utils_difficulty.py    # Difficulty prediction
├── config.py
├── models/                    # Trained ML models
├── data/                      # Game logs (scores, streaks, etc.)
├── music/                     # Game sounds
├── assets/                    # Images (crowns/icons)
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run

### 1. 📦 Install Requirements
```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 🤖 Train ML Models
```bash
python app/ml_data_generator.py
```

### 3. ▶️ Launch Game
```bash
python app/main.py
```

### 4. 🔬 Test ML Solver (CLI)
```bash
python app/test_ml_solver.py
```

---

## 📁 Output Files

| File                     | Description                                |
|--------------------------|--------------------------------------------|
| `scoreboard.txt`         | Logs of each completed level               |
| `streak.txt`             | Tracks daily streaks                       |
| `highscores.txt`         | Personal bests per board size              |
| `difficulty_data.csv`    | Training data for difficulty model         |
| `models/*.pkl`           | ML models for solving & recommending moves |

---

## 🧑‍💻 Built By

A team of Data Science Master's students committed to practical ML integration, creative UI design, and interactive learning:

- Stuti Bimali  
- Hrishabh Mahaju  
- Binaya Dhakal  
- Aayush Dongol  

---

## 📌 Future Enhancements

- [ ] Online user login with cloud-based scoreboard
- [ ] Android version (Flutter/Kivy with drag-and-drop)
- [ ] ML vs RL performance dashboard
- [ ] Deploy web version using Flask or Streamlit

---

## 📚 Educational Use Notice

This project is part of the DSCI 6003 Final Project: *"Mini Game with ML Integration"*  
You may use or reference this project for **educational and non-commercial purposes only**.

> © 2025 N-Queens ML Challenge Team. All rights reserved.

---

**Train your brain — every move counts! ♛**
