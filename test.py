# test.py
"""
Load models/savedmodel.pth and print LOADED_MODEL_TEST_ACCURACY: <value>
"""
import os
import joblib
from sklearn.metrics import accuracy_score

def main():
    model_file = os.path.join('models', 'savedmodel.pth')
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"{model_file} not found. Run train.py first.")
    data = joblib.load(model_file)
    clf = data['model']
    X_test = data['X_test']
    y_test = data['y_test']
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"LOADED_MODEL_TEST_ACCURACY: {acc:.4f}")

if __name__ == '__main__':
    main()
