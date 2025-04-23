import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure folders exist
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
