import pickle
from pathlib import Path


# Path to the root of the project
project_root = Path(__file__).parent.parent

# Path to the trained model file
model_path = project_root / 'assets' / 'model.pkl'


def load_model():
    """Load and return the machine learning model from disk."""
    with model_path.open('rb') as file:
        model = pickle.load(file)
    return model
