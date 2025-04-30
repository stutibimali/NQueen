import pandas as pd
import os
import pickle
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from config import DATA_DIR

df = pd.read_csv(os.path.join(DATA_DIR, "difficulty_data.csv"))

X = df[["board_size", "time_taken"]]
y = df["difficulty"]

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save model and encoder
with open(os.path.join(DATA_DIR, "difficulty_model.pkl"), "wb") as f:
    pickle.dump(clf, f)

with open(os.path.join(DATA_DIR, "difficulty_encoder.pkl"), "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Difficulty model trained and saved.")
