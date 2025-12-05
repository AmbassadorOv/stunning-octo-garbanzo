import pytest
import subprocess
import sys

def test_master_package_script_runs():
    """
    Runs the flag_master_package_knot_core.py script as a subprocess
    and checks that it exits with a code of 0 (success).
    """
    result = subprocess.run(
        [sys.executable, "-m", "src.flag_master_package_knot_core"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "KNOT CORE MASTER PACKAGE SEALED" in result.stdout
