"""
Tests for the saved model.
"""
import os
import joblib
from sklearn.metrics import accuracy_score

def test_model_loading_and_accuracy():
    """
    Loads the saved model and verifies its accuracy on the test set.
    """
    model_file = os.path.join('models', 'savedmodel.pth')
    assert os.path.exists(model_file), f"{model_file} not found. Run train.py first."

    data = joblib.load(model_file)
    clf = data['model']
    X_test = data['X_test']
    y_test = data['y_test']

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"LOADED_MODEL_TEST_ACCURACY: {acc:.4f}")
    assert acc > 0.8, "Model accuracy is below the 0.8 threshold."
