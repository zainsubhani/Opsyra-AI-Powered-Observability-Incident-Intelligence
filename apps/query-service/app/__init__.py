from pathlib import Path
import sys


shared_path = Path(__file__).resolve().parents[3] / "shared"
if str(shared_path) not in sys.path:
    sys.path.insert(0, str(shared_path))
