import pytest
from src import safe_placeholder_third_language
import subprocess
import sys

def test_safe_placeholder_script_runs():
    """
    Runs the safe_placeholder_third_language.py script as a subprocess
    and checks that it exits with a code of 0 (success).
    """
    result = subprocess.run(
        [sys.executable, "-m", "src.safe_placeholder_third_language"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "MASTER ORDER EXECUTED: SAFE PLACEHOLDER CREATED" in result.stdout
