import pytest
from src import operational_functions_layer
import subprocess
import sys

def test_operational_functions_layer_script_runs():
    """
    Runs the operational_functions_layer.py script as a subprocess
    and checks that it exits with a code of 0 (success).
    """
    result = subprocess.run(
        [sys.executable, "-m", "src.operational_functions_layer"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "MASTER DEPLOYMENT ORDER SEALED AND SAVED" in result.stdout
