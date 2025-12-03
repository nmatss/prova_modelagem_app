import sys
import os

# Add the parent directory to the path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    print("Attempting to import app...")
    from app import app
    print("Successfully imported app.")
except Exception as e:
    print(f"Failed to import app: {e}")
    import traceback
    traceback.print_exc()
