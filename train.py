# train.py
"""
Train a DecisionTreeClassifier on the Olivetti faces dataset.
Saves model + test split to models/savedmodel.pth
Prints TEST_ACCURACY: <value> for CI detection.
"""
import os
import joblib
import numpy as np
from sklearn.datasets import fetch_olivetti_faces
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def main():
    data = fetch_olivetti_faces(shuffle=True, random_state=42)
    X = data.data          # shape (400, 4096)
    y = data.target        # shape (400,)

    # 70% train, 30% test, with stratify so person distribution preserved
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.7, random_state=42, stratify=y
    )

    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    os.makedirs('models', exist_ok=True)
    joblib.dump({'model': clf, 'X_test': X_test, 'y_test': y_test}, 'models/savedmodel.pth')

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"TEST_ACCURACY: {acc:.4f}")

if __name__ == '__main__':
    main()
