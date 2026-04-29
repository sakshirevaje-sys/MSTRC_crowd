# train_model.py
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

DATA_PATH = "data/msrtc_crowd_data.csv" #data for training
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "crowd_rf_model.pkl")
PREPROCESS_PATH = os.path.join(MODEL_DIR, "preprocess.pkl")

def main():
    df = pd.read_csv(DATA_PATH)

    # Features and target
    feature_cols = [
        "route",
        "day_of_week",
        "hour",
        "is_weekend",
        "is_holiday",
        "is_festival",
        "distance_km",
        "num_stops",
        "weather",
    ]
    target_col = "crowd_level"

    X = df[feature_cols]
    y = df[target_col]

    # Categorical vs numerical
    categorical_features = ["route", "weather"]
    numeric_features = [
        "day_of_week",
        "hour",
        "is_weekend",
        "is_holiday",
        "is_festival",
        "distance_km",
        "num_stops",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numeric_features),
        ]
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)
    print(classification_report(y_test, y_pred))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")

if __name__ == "__main__":
    main()