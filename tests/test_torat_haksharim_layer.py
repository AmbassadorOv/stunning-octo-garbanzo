import pytest
from src import torat_haksharim_layer
import subprocess
import sys

def test_torat_haksharim_layer_script_runs():
    """
    Runs the torat_haksharim_layer.py script as a subprocess
    and checks that it exits with a code of 0 (success).
    """
    result = subprocess.run(
        [sys.executable, "-m", "src.torat_haksharim_layer"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "TORAT HAKSHARIM LAYER ACTIVATION" in result.stdout
