import pickle
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DATA_DIR

def predict_difficulty(board_size, time_taken):
    model_path = os.path.join(DATA_DIR, "difficulty_model.pkl")
    encoder_path = os.path.join(DATA_DIR, "difficulty_encoder.pkl")

    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        return "Unknown"

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(encoder_path, "rb") as f:
        encoder = pickle.load(f)

    pred = model.predict([[board_size, time_taken]])
    return encoder.inverse_transform(pred)[0]
