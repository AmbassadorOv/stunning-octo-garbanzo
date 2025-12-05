import pytest
import subprocess
import sys

def test_unified_architecture_script_runs_and_achieves_transitory_state():
    """
    Runs the unified_flag_architecture.py script as a subprocess and checks
    that it exits successfully and achieves the intended 'TRANSITORY STATE' (Wolf),
    as designed in the final provided model.
    """
    result = subprocess.run(
        [sys.executable, "-m", "src.unified_flag_architecture"],
        capture_output=True,
        text=True,
        # The script uses Hebrew characters, so ensure correct encoding
        encoding='utf-8'
    )

    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"
    assert "TRANSITORY STATE" in result.stdout
    assert "Wolf" in result.stdout
    assert "REALITY ACKNOWLEDGED" not in result.stdout # Ensure it's not the Lion state
