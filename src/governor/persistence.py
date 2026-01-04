import pickle
import os
from typing import Any

def seal_and_preserve(obj: Any, filename: str):
    """Generic function to seal and preserve any key component."""
    try:
        if hasattr(obj, 'seal') and callable(getattr(obj, 'seal')):
            obj.seal()

        with open(filename, 'wb') as f:
            pickle.dump(obj, f)
        print(f"💾 Component '{filename}' **SEALED & PRESERVED**.")
    except Exception as e:
        print(f"Error sealing/preserving {filename}: {e}")

def load_component(filename: str):
    """Generic function to load a preserved component."""
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, 'rb') as f:
            obj = pickle.load(f)
        return obj
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None
